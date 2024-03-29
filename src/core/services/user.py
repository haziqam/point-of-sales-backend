from typing import List, Optional, Tuple
from core.models.user import PublicUserData, Role, User
from core.repositories.user import IUserRepository
from security.hasher import IPasswordHasher
from exceptions.auth_exception import (
    InvalidCredentials,
    UserAlreadyExists,
    UserNotFound,
)


class UserService:
    def __init__(
        self, user_repository: IUserRepository, password_hasher: IPasswordHasher
    ) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def find_user_by_id(self, id: str) -> Optional[User]:
        return self.user_repository.find_user_by_id(id)

    def register(
        self, email: str, password: str, name: str, role: Role
    ) -> PublicUserData:
        """
        Raises:
        * UserAlreadyExists
        """
        existing_user = self.user_repository.find_user_by_email(email)
        if existing_user is not None:
            raise UserAlreadyExists()

        hashed_password = self.password_hasher.hash(password)
        new_user = self.user_repository.create_user(name, role, email, hashed_password)
        return new_user.public_data

    def login(self, email: str, password: str) -> PublicUserData:
        """
        Raises:
            * UserNotFound
            * InvalidCredentials
        """
        matching_user = self.user_repository.find_user_by_email(email)
        if matching_user is None:
            raise UserNotFound()

        success = self.password_hasher.verify(password, matching_user.hashed_password)
        if not success:
            raise InvalidCredentials()

        return matching_user.public_data

    def delete_user(self, user: User) -> None:
        self.user_repository.delete_user(user)

    def find_users(
        self,
        page: int = 1,
        number_per_page: int = 10,
        *,
        id: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        role: Optional[Role] = None,
    ) -> List[Tuple[PublicUserData, str]]:
        """
        Returns:
            A list of tuple containing the public user data
            and the user's email
        """
        users = self.user_repository.find_users(
            page, number_per_page, id=id, email=email, name=name, role=role
        )
        return list(map(lambda user: (user.public_data, user.email), users))
