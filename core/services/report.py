from datetime import datetime
from typing import Dict, List
from core.models.product import PurchasedProduct
from core.models.report import MonthlyReport
from core.repositories.bill import IBillRepository
from core.repositories.cash import ICashRepository
from core.repositories.member import IMemberRepository


class ReportService:
    def __init__(
        self,
        bill_repository: IBillRepository,
        member_repository: IMemberRepository,
        cash_repository: ICashRepository,
    ) -> None:
        self.bill_repository = bill_repository
        self.member_repository = member_repository
        self.cash_repository = cash_repository

    def get_purchased_products(
        self, start_date: datetime, end_date: datetime
    ) -> List[PurchasedProduct]:
        return self.bill_repository.get_purchased_products(start_date, end_date)

    def get_total_transactions(self, start_date: datetime, end_date: datetime) -> int:
        return self.bill_repository.get_total_transactions(start_date, end_date)

    def get_total_revenue(self, start_date: datetime, end_date: datetime) -> float:
        return self.bill_repository.get_total_revenue(start_date, end_date)

    def get_monthly_transactions(self, year: int) -> List[MonthlyReport[int]]:
        return self.bill_repository.get_monthly_transactions(year)

    def get_monthly_sold_products(self, year: int) -> List[MonthlyReport[int]]:
        return self.bill_repository.get_monthly_sold_products(year)

    def get_member_amount_by_type(self) -> Dict[str, int]:
        return self.member_repository.get_member_amount_by_type()

    def get_current_cash(self) -> float:
        return self.cash_repository.get_cash()
