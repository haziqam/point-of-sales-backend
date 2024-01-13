from abc import ABC, abstractmethod
from typing import Callable, TypeVar

T = TypeVar("T")


class ITransactionProvider(ABC):
    @abstractmethod
    def transact(self, callback: Callable[..., T]) -> T:
        pass
