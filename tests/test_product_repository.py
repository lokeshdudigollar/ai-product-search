from src.repositories.product_repository import ProductRepository


def test_search_by_price():
    repo = ProductRepository("src/repositories/data/products.json")

    results = repo.search(max_price=80)

    assert all(p.price <= 80 for p in results)


def test_search_by_vehicle():
    repo = ProductRepository("src/repositories/data/products.json")

    results = repo.search(vehicle="Toyota")

    assert all("toyota" in p.vehicle.lower() for p in results)