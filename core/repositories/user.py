
from abc import ABC, abstractmethod
from typing import Optional
from core.models.user import Role, User

class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, name: str, role: Role, email: str, hashed_password: str) -> User:
        pass

    @abstractmethod
    def find_user_by_id(self, id: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user:User) -> None:
        pass