from fastapi import FastAPI
from src.api.search import router as search_router

app = FastAPI(title="AI Product Search Assistant")

app.include_router(search_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}