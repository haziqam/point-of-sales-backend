from fastapi import APIRouter
from core.services.report import ReportService


class ReportController(APIRouter):
    def __init__(self, report_service: ReportService) -> None:
        super().__init__(prefix="/report")
        self.report_service = report_service

    # def _assign_routes(self):
    #     async def get_products_report
