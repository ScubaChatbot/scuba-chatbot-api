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

def generate_rag_answer(state: MessagesState):
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