
from abc import ABC, abstractmethod
from typing import Optional
from core.models.user import Role, User

class IUserRepository(ABC):
    @abstractmethod
    def create_user(name: str, role: Role, email: str, hashed_password: str) -> User:
        pass

    @abstractmethod
    def find_user_by_id(id: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_user_by_email(email: str) -> Optional[User]:
        pass

    @abstractmethod
    def update_user(user: User) -> User:
        pass

    @abstractmethod
    def delete_user(user:User) -> None:
        pass