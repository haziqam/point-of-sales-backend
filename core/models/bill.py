from datetime import datetime
from typing import List
from pydantic import BaseModel
from core.models.product import PurchasedProduct


class Bill(BaseModel):
    id: str
    transaction_date: datetime
    purchased_products: List[PurchasedProduct]
    subtotal_price: float
    points_used: float = 0.0
    discount: float = 0.0
    total_price: float
