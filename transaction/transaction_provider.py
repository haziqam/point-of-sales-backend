from abc import ABC, abstractmethod
from typing import Callable, TypeVar

T = TypeVar("T")


class ITransactionProvider(ABC):
    @abstractmethod
    def transact(self, callback: Callable[..., T]) -> T:
        pass


class ConcreteTransactionProvider(ITransactionProvider):
    def transact(self, callback: Callable[..., T]) -> T:
        print("Transaction started")
        retval = None
        # Technical details of transaction here...
        # with start_transaction() as blah:
        # retval = callback()
        session = 10
        retval = callback(session=session)  # for the sake of simplicity
        print("Transaction committed")
        return retval


class TransactionConsumer:
    def __init__(self, transaction_provider: ITransactionProvider) -> None:
        self.transaction_provider = transaction_provider

    def _something(self, a: int, b: int, **kwargs) -> int:
        print(f"Hello {a}")
        print(f"Hello {b}")
        print(f"Using kwargs session here: {kwargs['session']}")
        return a + b

    def something(self, a: int, b: int) -> int:
        callback = lambda session: self._something(a, b, session=session)
        return self.transaction_provider.transact(callback)


# tp = ConcreteTransactionProvider()
# tc = TransactionConsumer(tp)
# ret_value = tc.something(3, 5)
# print(f"return value: {ret_value}")
