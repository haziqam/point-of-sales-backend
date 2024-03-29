from abc import ABC, abstractmethod


class ICashRepository(ABC):
    @abstractmethod
    def get_cash(self, **kwargs) -> float:
        pass

    @abstractmethod
    def add_cash(self, amount: float, **kwargs) -> None:
        pass

    @abstractmethod
    def subtract_cash(self, amount: float, **kwargs) -> None:
        pass

    @abstractmethod
    def is_sufficient(self, amount: float, **kwargs) -> bool:
        pass
