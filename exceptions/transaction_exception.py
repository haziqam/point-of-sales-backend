class TransactionException(Exception):
    pass


class InsufficientStock(TransactionException):
    pass


class InsufficientPoint(TransactionException):
    pass
