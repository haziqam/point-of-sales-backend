from core.repositories.bill import IBillRepository
from core.repositories.product import IProductRepository


class ReportService:
    def __init__(self, product_repository: IProductRepository, bill_repository: IBillRepository) -> None:
        self.product_repository = product_repository
        self.bill_repository = bill_repository

    # TODO: define methods