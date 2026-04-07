from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from src.models.product import Product
from src.repositories.product_repository import ProductRepository
from src.core.dependencies import get_product_repository

router = APIRouter()


@router.get("/search", response_model=List[Product])
def search_products(
    query: Optional[str] = None,
    max_price: Optional[float] = Query(None),
    brand: Optional[str] = None,
    vehicle: Optional[str] = None,
    repo: ProductRepository = Depends(get_product_repository),
):
    return repo.search(query, max_price, brand, vehicle)

from src.services.search_service import SearchService
from src.models.search import SearchRequest, SearchResponse

@router.post("/ai-search", response_model=SearchResponse)
def ai_search(
    request: SearchRequest,
    repo: ProductRepository = Depends(get_product_repository),
):
    service = SearchService(repo)

    results = service.search(request.query)

    return {"results": results}