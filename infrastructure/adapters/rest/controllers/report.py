from datetime import datetime
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends
from core.models.product import Product, PurchasedProduct
from core.models.report import MonthlyReport
from core.services.inventory import InventoryService
from core.services.report import ReportService
from infrastructure.adapters.rest.middlewares.manager_auth import (
    manager_auth_middleware,
)


class ReportController(APIRouter):
    def __init__(
        self, report_service: ReportService, inventory_service: InventoryService
    ) -> None:
        super().__init__(prefix="/report")
        self.report_service = report_service
        self.inventory_service = inventory_service
        self._assign_routes()

    def _assign_routes(self):
        @self.get(
            "/purchased-products", dependencies=[Depends(manager_auth_middleware)]
        )
        def get_purchased_products(
            start_date: datetime, end_date: datetime
        ) -> List[PurchasedProduct]:
            return self.report_service.get_purchased_products(start_date, end_date)

        @self.get(
            "/total_transactions", dependencies=[Depends(manager_auth_middleware)]
        )
        def get_total_transactions(start_date: datetime, end_date: datetime) -> int:
            return self.report_service.get_total_transactions(start_date, end_date)

        @self.get("/total-revenue", dependencies=[Depends(manager_auth_middleware)])
        def get_total_revenue(start_date: datetime, end_date: datetime) -> float:
            return self.report_service.get_total_revenue(start_date, end_date)

        @self.get(
            "/monthly_transactions", dependencies=[Depends(manager_auth_middleware)]
        )
        def get_monthly_transactions(year: int) -> List[MonthlyReport[int]]:
            return self.report_service.get_monthly_transactions(year)

        @self.get(
            "/monthly-sold-products", dependencies=[Depends(manager_auth_middleware)]
        )
        def get_monthly_sold_products(year: int) -> List[MonthlyReport[int]]:
            return self.report_service.get_monthly_sold_products(year)

        @self.get(
            "/member-amount-by-type", dependencies=[Depends(manager_auth_middleware)]
        )
        def get_member_amount_by_type() -> Dict[str, int]:
            return self.report_service.get_member_amount_by_type()

        @self.get("current-cash", dependencies=[Depends(manager_auth_middleware)])
        def get_current_cash() -> float:
            return self.report_service.get_current_cash()

        @self.get(
            "/out-of-stock-products", dependencies=[Depends(manager_auth_middleware)]
        )
        def get_out_of_stock_products(
            page: int = 1, number_per_page: int = 10
        ) -> List[Product]:
            return self.inventory_service.find_products(
                page=page, number_per_page=number_per_page, stock=0
            )
