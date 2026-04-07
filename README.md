# AI Product Search Assistant (RAG-based)

An intelligent product search system that uses **Retrieval-Augmented Generation (RAG)** to understand user queries and return relevant product recommendations.

---

## Features

- **Semantic Search (FAISS)** — understands intent, not just keywords
- **LLM-powered reasoning** — generates contextual recommendations
- **Hybrid Retrieval** — vector search + filtering + ranking
- **Structured Output** — reliable JSON responses
- **Fault Tolerance** — fallback when LLM fails
- **Prompt Versioning** — safe iteration of LLM behavior
- **Caching Layer** — optimized repeated queries
- **Testable Architecture** — dependency injection + mocking

---

## Architecture

```text
Client (API Request)
        ↓
FastAPI (API Layer)
        ↓
SearchService (Business Logic)
        ↓
-----------------------------------
| Query Parser (LLM)              |
| Vector Search (FAISS)           |
| Ranking Layer                   |
| Prompt Versioning               |
-----------------------------------
        ↓
LLM (OpenAI)
        ↓
Structured JSON Response
```

---

````mermaid
flowchart TD
    A[User Query] --> B[FastAPI]
    B --> C[SearchService]

    C --> D[Query Parser]
    C --> E[Vector Search (FAISS)]
    C --> F[Ranking Layer]

    E --> F
    F --> G[Prompt Versioning]

    G --> H[LLM]
    H --> I[Structured JSON Response]

    C --> J[Cache]


---
## Tech Stack

- **Backend**: FastAPI
- **LLM**: OpenAI (via LangChain)
- **Vector Search**: FAISS
- **Embeddings**: Sentence Transformers
- **Testing**: Pytest
- **Logging**: Loguru

---

## Setup
```bash
git clone <your-repo>
cd ai-product-search
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

---

## Environment Variables

Create `.env`:

```env
OPENAI_API_KEY=your_key
MODEL_NAME=gpt-4o-mini
USE_LLM=false
PROMPT_VERSION=v2
```

---

## how to run locally

```bash
uvicorn src.main:app --reload
```

---

## Run Tests

```bash
pytest
```

---

## 📡 API Endpoints

### Health Check

```
GET /health
```

### AI Search

```
POST /ai-search
```

#### Example Request:

```json
{
  "query": "Find brake pads under 100 for Toyota"
}
```

---

## How It Works

1. Parse user query → structured filters
2. Perform semantic search using FAISS
3. Apply filters (price, brand, vehicle)
4. Rank products based on relevance
5. Generate response using LLM
6. Return structured JSON

---

## Key Engineering Highlights

- Clean Architecture (separation of concerns)
- Dependency Injection (testability)
- Hybrid Retrieval (semantic + rule-based)
- Resilient LLM integration (fallback + retry)
- Config-driven system (env-based control)

---

## Future Improvements

- Redis caching
- Streaming responses
- LLM evaluation metrics
- Multi-agent workflows
