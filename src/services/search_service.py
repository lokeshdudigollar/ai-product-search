import time
from typing import List

from src.repositories.product_repository import ProductRepository
from src.rag.query_parser import parse_query
from src.services.llm_provider import LLMProvider
from src.utils.json_parser import safe_json_loads
from src.utils.retry import retry
from src.core.logger import get_logger
from langchain_core.prompts import ChatPromptTemplate
from src.services.ranking_service import rank_products
from src.rag.prompts import PROMPTS
from src.utils.cache import get_cache, set_cache

logger = get_logger()


class SearchService:
    def __init__(self, repo: ProductRepository, llm_provider: LLMProvider):
        self.repo = repo
        self.llm_provider = llm_provider
        self.vector_store = vector_store
        self.embedder = embedder

    def search(self, user_query: str) -> List[dict]:
        start_time = time.time()

        logger.info(f"Search started: {user_query}")

        # Parse query
        filters = parse_query(user_query)
        logger.info(f"Parsed filters: {filters}")
        
        cached = get_cache(user_query)
        if cached:
            return cached
        
        #  Hybrid Retrieval (Vector + Filter)

        # 1. Semantic search
        query_vector = self.embedder.embed([user_query])[0]
        semantic_results = self.vector_store.search(query_vector, k=10)

        # 2.Apply filters
        products = [
            p for p in semantic_results
            if (not filters.get("max_price") or p.price <= filters.get("max_price"))
            and (not filters.get("brand") or filters["brand"].lower() in p.brand.lower())
            and (not filters.get("vehicle") or filters["vehicle"].lower() in p.vehicle.lower())
        ]

        # 3. ranking
        products = rank_products(products, user_query)

        logger.info(f"Products retrieved: {len(products)}")

        if not products:
            return []

        context = "\n".join([
            f"{p.id} | {p.name} | ${p.price} | {p.description}"
            for p in products
        ])

        prompt_template = PROMPTS["v2"]
        prompt = ChatPromptTemplate.from_template(prompt_template)

        chain = prompt | self.llm_provider.llm

        def llm_call():
            response = self.llm_provider.invoke(chain, {
                "query": user_query,
                "context": context
            })
            return response.content

        # Retry LLM
        raw_output = retry(llm_call)

        logger.info(f"LLM raw output: {raw_output}")

        # Safe parse
        results = safe_json_loads(raw_output, [])

        set_cache(user_query, results)

        duration = time.time() - start_time
        logger.info(f"Search completed in {duration:.2f}s")

        return results