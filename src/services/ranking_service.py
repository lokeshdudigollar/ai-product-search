def score_product(product, query: str):
    score = 0

    if query.lower() in product.name.lower():
        score += 3

    if query.lower() in product.description.lower():
        score += 2

    # cheaper = better (example logic)
    score += max(0, 100 - product.price) / 100

    return score


def rank_products(products, query: str):
    return sorted(products, key=lambda p: score_product(p, query), reverse=True)