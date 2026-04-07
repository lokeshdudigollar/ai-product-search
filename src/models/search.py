from pydantic import BaseModel
from typing import List, Optional


class SearchRequest(BaseModel):
    query: str


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    reason: str


class SearchResponse(BaseModel):
    results: List[ProductResponse]