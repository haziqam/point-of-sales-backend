from abc import ABC, abstractmethod

class ICashRepository(ABC):
    @abstractmethod
    def get_cash(self) -> float:
        pass

    @abstractmethod
    def add_cash(self, amount: float) -> None:
        pass

    @abstractmethod
    def subtract_cash(self, amount: float) -> None:
        pass

    @abstractmethod
    def is_sufficient(self, amount: float) -> bool:
        pass 