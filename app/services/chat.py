from dotenv import load_dotenv
import glob

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langgraph.graph import MessagesState
from langchain.chat_models import init_chat_model

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
        return
    
    try:
        # Initialize chat model
        response_model = init_chat_model(MODEL_NAME, temperature=MODEL_TEMPERATURE)

        # Load and process documents
        paths = glob.glob("knowledge_base/*.yaml")
        docs = [TextLoader(path).load() for path in paths]
        document_list = [item for sublist in docs for item in sublist]

        # Split documents for vector storage
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=100, chunk_overlap=50
        )
        docs_splits = text_splitter.split_documents(document_list)

        # Create in-memory vector store and retriever
        vectorstore = InMemoryVectorStore.from_documents(
            documents=docs_splits, embedding=OpenAIEmbeddings()
        )
        retriever = vectorstore.as_retriever()

        # Create retriever tool
        retriever_tool = create_retriever_tool(
            retriever,
            "retrieve_blog_posts",
            "Buscador de información basada en experiencias de viajes de buceo por Colombia",
        )
        
        is_initialized = True
        print("Chat service initialized successfully")
        
    except Exception as e:
        print(f"Failed to initialize chat service: {e}")
        print("Chat functionality will be unavailable")

def generate_rag_answer(state: MessagesState):
    """Generate RAG answer with initialization check"""
    global response_model, retriever_tool, is_initialized
    
    # Initialize if not already done
    if not is_initialized:
        initialize_chat_service()
    
    # Check if initialization was successful
    if not is_initialized or response_model is None or retriever_tool is None:
        return {"messages": [{"role": "assistant", "content": "Lo siento, el servicio de chat no está disponible en este momento."}]}
    
    try:
        query = state["messages"][-1]["content"]
        docs = retriever_tool.invoke({"query": query})
        full_prompt = (
            "Rol:Eres un asistente de buceo en Colombia, educado y enfocado en el cliente. "
            "Siempre debes responder de manera amable y servicial.\n\n"
            f"Contexto:\n{docs}\n\n"
            f"Pregunta del usuario: {query}"
        )
        response = response_model.invoke(full_prompt)
        return {"messages": [response]}
        
    except Exception as e:
        print(f"Error generating response: {e}")
        return {"messages": [{"role": "assistant", "content": "Lo siento, ocurrió un error al procesar tu consulta."}]}
