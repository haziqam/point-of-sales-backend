from abc import ABC, abstractmethod
from typing import Dict, Optional
from core.models.member import Member


class IMemberRepository(ABC):
    @abstractmethod
    def create_member(
        self, email: str, hashed_PIN: str, name: str, points: float = 0.0, **kwargs
    ) -> Member:
        pass

    @abstractmethod
    def find_member_by_id(self, id: str, **kwargs) -> Optional[Member]:
        pass

    @abstractmethod
    def find_member_by_email(self, email: str, **kwargs) -> Optional[Member]:
        pass

    @abstractmethod
    def update_member(self, member: Member, **kwargs) -> Member:
        pass

    @abstractmethod
    def delete_member(self, member: Member, **kwargs) -> None:
        pass

    @abstractmethod
    def get_member_amount_by_type(self, **kwargs) -> Dict[str, int]:
        """
        Returns:
            A dictionary with member type as the key and amount as the value
        """
        pass
