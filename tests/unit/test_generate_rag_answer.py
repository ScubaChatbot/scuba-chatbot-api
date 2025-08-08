import pytest
from app.services.chat import generate_rag_answer

class DummyRetriever:
    def invoke(self, query):
        return "Dummy context"

class DummyLLM:
    def invoke(self, prompt):
        return {"role": "assistant", "content": f"Echo: {prompt}"}

def test_generate_rag_answer_unit():
    """
    Unit test for generate_rag_answer with injected dummy retriever and llm.
    Ensures no real LLM or retrieval is called.
    """
    state = {"messages": [{"role": "user", "content": "What is the schedule?"}]}
    result = generate_rag_answer(state, retriever=DummyRetriever(), llm=DummyLLM())
    assert "messages" in result
    assert result["messages"][0]["content"].startswith("Echo: ")
