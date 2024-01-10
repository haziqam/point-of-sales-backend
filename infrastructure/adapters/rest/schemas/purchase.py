from typing import List, Optional
from pydantic import BaseModel, validator


class ProductPurchaseSchema(BaseModel):
    id: str
    amount: int

    @validator("amount")
    def validate_amount(cls, value: int):
        if value <= 0:
            raise ValueError("Product amount must be at least one")
        return value


class PurchaseSchema(BaseModel):
    products: List[ProductPurchaseSchema]
    member_id: Optional[str]
    points_used: Optional[float]

    @validator("points_used")
    def validate_points_used(cls, value: Optional[float]):
        if value is not None and value < 0:
            raise ValueError("Negative points are not allowed")
        return value
