from abc import ABC, abstractmethod

class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abstractmethod
    def verify(entered_password: str, stored_password: str) -> bool:
        pass