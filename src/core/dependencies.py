from src.repositories.product_repository import ProductRepository


def get_product_repository() -> ProductRepository:
    return ProductRepository("src/repositories/data/products.json")