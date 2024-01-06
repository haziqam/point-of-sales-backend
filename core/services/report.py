from core.repositories.bill import IBillRepository
from core.repositories.product import IProductRepository
from transaction.transaction_provider import ITransactionProvider


class ReportService:
    def __init__(
        self,
        product_repository: IProductRepository,
        bill_repository: IBillRepository,
        transaction_provider: ITransactionProvider,
    ) -> None:
        self.product_repository = product_repository
        self.bill_repository = bill_repository
        self.transaction_provider = transaction_provider

    # TODO: define methods
