import pytest
from app.services import chat as chat_service

class DummyRetriever:
    def invoke(self, query):
        return "Dummy context"

class DummyLLM:
    def invoke(self, prompt):
        return {"role": "assistant", "content": f"Echo: {prompt}"}

def test_generate_rag_answer_known_query():
    """
    Test generate_rag_answer with a known query using dummy retriever and llm (no real LLM call).
    """
    state = {"messages": [{"role": "user", "content": "¿Cuál es el horario?"}]}
    result = chat_service.generate_rag_answer(state, retriever=DummyRetriever(), llm=DummyLLM())
    assert result is not None
    assert "messages" in result
    assert isinstance(result["messages"], list)
    assert result["messages"][0]["content"].startswith("Echo: ")

def test_generate_rag_answer_unknown_query():
    """
    Test generate_rag_answer with an unknown query using dummy retriever and llm (no real LLM call).
    """
    state = {"messages": [{"role": "user", "content": "¿Qué es AtlantisX?"}]}
    result = chat_service.generate_rag_answer(state, retriever=DummyRetriever(), llm=DummyLLM())
    assert result is not None
    assert "messages" in result
    assert isinstance(result["messages"], list)
    assert result["messages"][0]["content"].startswith("Echo: ")
