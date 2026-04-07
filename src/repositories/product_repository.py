import json
from typing import List, Optional
from pathlib import Path

from src.models.product import Product


class ProductRepository:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._products = self._load_products()

    def _load_products(self) -> List[Product]:
        with open(self.file_path, "r") as f:
            data = json.load(f)
        return [Product(**item) for item in data]

    def get_all(self) -> List[Product]:
        return self._products

    def search(
        self,
        query: Optional[str] = None,
        max_price: Optional[float] = None,
        brand: Optional[str] = None,
        vehicle: Optional[str] = None,
    ) -> List[Product]:
        results = self._products

        if query:
            query_lower = query.lower()
            results = [
                p for p in results
                if query_lower in p.name.lower()
                or query_lower in p.description.lower()
                or query_lower in p.category.lower()
            ]

        if max_price is not None:
            results = [p for p in results if p.price <= max_price]

        if brand:
            results = [p for p in results if brand.lower() in p.brand.lower()]

        if vehicle:
            results = [
                p for p in results
                if vehicle.lower() in p.vehicle.lower()
            ]

        return results