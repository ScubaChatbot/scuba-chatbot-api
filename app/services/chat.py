from dotenv import load_dotenv
import glob
import logging

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langgraph.graph import MessagesState
from langchain.chat_models import init_chat_model


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Model configuration
MODEL_NAME = "openai:gpt-4.1"
MODEL_TEMPERATURE = 0

# Global variables
response_model = None
retriever_tool = None
is_initialized = False

def initialize_chat_service():
    """Initialize OpenAI chat service and RAG components"""
    global response_model, retriever_tool, is_initialized
    
    if is_initialized:
        logger.info("Chat service already initialized.")
        return

    try:
        logger.info("Initializing chat model...")
        response_model = init_chat_model(MODEL_NAME, temperature=MODEL_TEMPERATURE)

        logger.info("Loading and processing knowledge base documents...")
        paths = glob.glob("knowledge_base/*.yaml")
        docs = [TextLoader(path).load() for path in paths]
        document_list = [item for sublist in docs for item in sublist]

        logger.info("Splitting documents for vector storage...")
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=100, chunk_overlap=50
        )
        docs_splits = text_splitter.split_documents(document_list)

        logger.info("Creating in-memory vector store and retriever...")
        vectorstore = InMemoryVectorStore.from_documents(
            documents=docs_splits, embedding=OpenAIEmbeddings()
        )
        retriever = vectorstore.as_retriever()

        logger.info("Creating retriever tool...")
        retriever_tool = create_retriever_tool(
            retriever,
            "retrieve_blog_posts",
            "Buscador de información basada en experiencias de viajes de buceo por Colombia",
        )
        is_initialized = True
        logger.info("Chat service initialized successfully.")

    except Exception as e:
        logger.error(f"Failed to initialize chat service: {e}")
        logger.error("Chat functionality will be unavailable.")

def generate_rag_answer(state: MessagesState):
    """Generate RAG answer with initialization check"""
    global response_model, retriever_tool, is_initialized
    
    # Initialize if not already done
    if not is_initialized:
        logger.info("Chat service not initialized. Initializing now...")
        initialize_chat_service()

    # Check if initialization was successful
    if not is_initialized or response_model is None or retriever_tool is None:
        logger.error("Chat service unavailable: retriever or response model not initialized.")
        return {"messages": [{"role": "assistant", "content": "Sorry, the chat service is currently unavailable."}]}

    try:
        query = state["messages"][-1]["content"]
        logger.info(f"Received user query: {query}")
        docs = retriever_tool.invoke({"query": query})
        logger.info("Retrieved context from knowledge base.")
        full_prompt = (
            "Rol:Eres un asistente de buceo en Colombia, educado y enfocado en el cliente. "
            "Siempre debes responder de manera amable y servicial.\n\n"
            f"Contexto:\n{docs}\n\n"
            f"Pregunta del usuario: {query}"
        )
        logger.info("Sending prompt to LLM.")
        response = response_model.invoke(full_prompt)
        logger.info("LLM response generated successfully.")
        return {"messages": [response]}

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return {"messages": [{"role": "assistant", "content": "Sorry, an error occurred while processing your request."}]}
