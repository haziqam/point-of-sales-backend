
from abc import ABC, abstractmethod
from typing import List
from core.models.bill import Bill
from core.models.product import PurchasedProduct

class IBillRepository(ABC):
    @abstractmethod
    def create_bill(self, transaction_date: str, purchased_products: List[PurchasedProduct], 
            total_price: float, memberId: str = None) -> Bill:
        pass