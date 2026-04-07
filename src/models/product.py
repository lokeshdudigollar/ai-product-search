from pydantic import BaseModel

class Product(BaseModel):
    id: str
    name: str
    brand: str
    category: str
    price: float
    vehicle: str
    description: str