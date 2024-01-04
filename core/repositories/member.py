from abc import ABC, abstractmethod
from typing import Optional
from core.models.member import Member


class IMemberRepository(ABC):
    @abstractmethod
    def create_member(id: str, email: str, hashed_PIN: str, name: str, points: float = 0.0) -> Member:
        pass

    @abstractmethod
    def find_member_by_id(id: str) -> Optional[Member]:
        pass

    @abstractmethod
    def find_member_by_email(email: str) -> Optional[Member]:
        pass

    @abstractmethod
    def update_member(member: Member) -> Member:
        pass

    @abstractmethod
    def delete_member(member: Member) -> None:
        pass
