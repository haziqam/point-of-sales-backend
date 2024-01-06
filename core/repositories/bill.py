from abc import ABC, abstractmethod
from typing import List
from core.models.bill import Bill
from core.models.product import PurchasedProduct


class IBillRepository(ABC):
    @abstractmethod
    def create_bill(
        self,
        transaction_date: str,
        purchased_products: List[PurchasedProduct],
        subtotal_price: float,
        total_price: float,
        points_used: float = 0.0,
        discount: float = 0.0,
        **kwargs
    ) -> Bill:
        pass
