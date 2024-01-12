from typing import Callable, Optional, TypeVar

from pymongo import MongoClient
from transaction.transaction_provider import ITransactionProvider

T = TypeVar("T")


class MongoDBTransactionProvider(ITransactionProvider):
    def __init__(self, client: MongoClient) -> None:
        super().__init__()
        self.client = client

    def transact(self, callback: Callable[..., T]) -> Optional[T]:
        retval = None
        with self.client.start_session() as session:
            with session.start_transaction():
                retval = callback(session=session)

        return retval
