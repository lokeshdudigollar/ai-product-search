from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_ai_search_basic(monkeypatch):

    class MockLLM:
        def invoke(self, payload):
            class Response:
                content = '[{"id": "P001", "name": "Mock Product", "price": 50, "reason": "Good match"}]'
            return Response()

    class MockLLMProvider:
        def __init__(self):
            self.llm = None  # not used

        def invoke(self, chain, payload):
            return MockLLM().invoke(payload)

    import src.api.search as search_module

    monkeypatch.setattr(search_module, "LLMProvider", MockLLMProvider)

    response = client.post("/ai-search", json={
        "query": "brake pads under 100"
    })

    assert response.status_code == 200
    assert len(response.json()["results"]) > 0