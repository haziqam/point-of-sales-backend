from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List
from core.models.bill import Bill
from core.models.product import PurchasedProduct
from core.models.report import MonthlyReport


class IBillRepository(ABC):
    @abstractmethod
    def create_bill(
        self,
        transaction_date: datetime,
        purchased_products: List[PurchasedProduct],
        subtotal_price: float,
        total_price: float,
        points_used: float = 0.0,
        discount: float = 0.0,
        **kwargs
    ) -> Bill:
        pass

    # @abstractmethod
    # def get_purchased_products(
    #     self, start_date: datetime, end_date: datetime, **kwargs
    # ) -> List[PurchasedProduct]:
    #     pass

    # @abstractmethod
    # def get_total_transactions(
    #     self, start_date: datetime, end_date: datetime, **kwargs
    # ) -> int:
    #     pass

    # @abstractmethod
    # def get_total_revenue(
    #     self, start_date: datetime, end_date: datetime, **kwargs
    # ) -> float:
    #     pass

    # @abstractmethod
    # def get_monthly_transactions(self, year: int) -> List[MonthlyReport[int]]:
    #     pass

    # @abstractmethod
    # def get_monthly_sold_products(self, year: int) -> List[MonthlyReport[int]]:
    #     pass
