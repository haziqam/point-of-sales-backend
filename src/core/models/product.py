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

    @classmethod
    def create_from_product(cls, product: Product, amount: int) -> "PurchasedProduct":
        purchased_product = cls(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            amount=amount,
        )
        return purchased_product
