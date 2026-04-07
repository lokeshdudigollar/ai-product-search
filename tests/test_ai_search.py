from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app
import json
from langchain_core.messages import AIMessage

client = TestClient(app)

def test_ai_search_basic():
    mock_responses = [
        AIMessage(content=json.dumps({"query": "brake pads", "max_price": 100, "vehicle": "Toyota"})),
        AIMessage(content=json.dumps([{"id": "P001", "name": "Toyota Corolla Brake Pads", "price": 75.0, "reason": "Fits Toyota"}]))
    ]
    
    with patch("langchain_openai.ChatOpenAI.invoke", side_effect=mock_responses):
        response = client.post("/ai-search", json={
            "query": "brake pads under 100 for Toyota"
        })

    assert response.status_code == 200
    assert "results" in response.json()