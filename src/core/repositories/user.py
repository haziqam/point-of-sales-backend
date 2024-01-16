from abc import ABC, abstractmethod
from typing import List, Optional
from core.models.user import Role, User


class IUserRepository(ABC):
    @abstractmethod
    def create_user(
        self, name: str, role: Role, email: str, hashed_password: str, **kwargs
    ) -> User:
        pass

    @abstractmethod
    def find_user_by_id(self, id: str, **kwargs) -> Optional[User]:
        pass

    @abstractmethod
    def find_user_by_email(self, email: str, **kwargs) -> Optional[User]:
        pass

    @abstractmethod
    def find_users(
        self,
        page: int = 1,
        number_per_page: int = 10,
        *,
        id: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        role: Optional[Role] = None,
        **kwargs
    ) -> List[User]:
        pass

    @abstractmethod
    def update_user(self, user: User, **kwargs) -> User:
        pass

    @abstractmethod
    def delete_user(self, user: User, **kwargs) -> None:
        pass
