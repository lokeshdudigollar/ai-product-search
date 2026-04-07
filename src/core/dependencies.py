from src.repositories.product_repository import ProductRepository
from src.services.llm_provider import LLMProvider

def get_product_repository() -> ProductRepository:
    return ProductRepository("src/repositories/data/products.json")

def get_llm_provider():
    return LLMProvider()