from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langgraph.graph import MessagesState
from langchain.chat_models import init_chat_model
import glob


load_dotenv()

model_temperature = 0
response_model = init_chat_model("openai:gpt-4.1", temperature=model_temperature)

paths = glob.glob("knowledge_base/*.yaml")
docs = [TextLoader(path).load() for path in paths]
document_list = [item for sublist in docs for item in sublist]
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)
docs_splits = text_splitter.split_documents(document_list)
docs_splits[5].page_content.strip()

vectorstore = InMemoryVectorStore.from_documents(
    documents=docs_splits, embedding=OpenAIEmbeddings()
)

retriever = vectorstore.as_retriever()
retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_blog_posts",
    "Buscador de información basada en experiencias de viajes de buceo por Colombia",
)

def generate_rag_answer(state: MessagesState):
    docs = retriever_tool.invoke({"query": state["messages"][-1]["content"]})
    full_prompt = f'Contexto:\n{docs}\n\nPregunta del usuario: { state["messages"][-1]["content"] }'
    response = response_model.invoke(full_prompt)
    return {"messages": [response]}