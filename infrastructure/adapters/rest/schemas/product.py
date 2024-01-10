from typing import Optional
from pydantic import BaseModel, validator


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    stock: int

    @validator("price")
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        return value

    @validator("stock")
    def validate_stock(cls, value):
        if value < 0:
            raise ValueError("Stock cannot be negative")
        return value


class UpdateProductSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

    @validator("price")
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        return value

    @validator("stock")
    def validate_stock(cls, value):
        if value < 0:
            raise ValueError("Stock cannot be negative")
        return value
