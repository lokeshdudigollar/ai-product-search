from src.repositories.product_repository import ProductRepository
from src.services.embedding_service import EmbeddingService
from src.repositories.vector_store import VectorStore


def build_vector_store(repo: ProductRepository):
    embedder = EmbeddingService()

    products = repo.get_all()

    texts = [
        f"{p.name} {p.description} {p.category} {p.vehicle}"
        for p in products
    ]

    vectors = embedder.embed(texts)

    store = VectorStore(len(vectors[0]))
    store.add(vectors, products)

    return store