from typing import List

from src.repositories.product_repository import ProductRepository
from src.rag.query_parser import parse_query
from src.models.product import Product

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.core.config import settings
import json


class SearchService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo
        self.llm = ChatOpenAI(
            temperature=0.3,
            openai_api_key=settings.OPENAI_API_KEY,
            model=settings.MODEL_NAME,
        )

    def search(self, user_query: str) -> List[dict]:
        # Step 1: Parse query
        filters = parse_query(user_query)

        # Step 2: Retrieve products
        products = self.repo.search(
            query=filters.get("query"),
            max_price=filters.get("max_price"),
            brand=filters.get("brand"),
            vehicle=filters.get("vehicle"),
        )

        # Step 3: Build context
        context = "\n".join([
            f"{p.name} - ${p.price} - {p.description}"
            for p in products
        ])

        # Step 4: LLM reasoning
        prompt = ChatPromptTemplate.from_template(
            """
            You are an e-commerce assistant.

            Based on user query and product list, return best matches.

            Return JSON:
            [
            {{"id": "...", "name": "...", "price": number, "reason": "..."}}
            ]

            User Query:
            {query}

            Products:
            {context}
            """
        )

        chain = prompt | self.llm
        response = chain.invoke({
            "query": user_query,
            "context": context
        })

        try:
            return json.loads(response.content)
        except Exception:
            return []