from transaction.transaction_provider import ITransactionProvider


class TransactionContainer:
    def __init__(self, transaction_provider: ITransactionProvider) -> None:
        self.transaction_provider = transaction_provider
