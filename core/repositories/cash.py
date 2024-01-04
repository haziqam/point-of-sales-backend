from abc import ABC, abstractmethod

class ICashRepository(ABC):
    @abstractmethod
    def get_cash() -> float:
        pass

    @abstractmethod
    def add_cash(amount: float) -> None:
        pass

    @abstractmethod
    def subtract_cash(amount: float) -> None:
        pass

    @abstractmethod
    def is_sufficient(amount: float) -> bool:
        pass 