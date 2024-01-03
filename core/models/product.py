from pydantic import BaseModel

class BaseProduct(BaseModel):
    id: str
    name: str
    description: str
    price: float

class Product(BaseProduct):
    stock: int

class PurchasedProduct(BaseProduct):
    amount: int
