from core.models.user import PublicUserData, Role
from core.repositories.user import IUserRepository
from core.security.hasher import IPasswordHasher
from exceptions.auth_exception import InvalidCredentials, UserNotFound


class UserService:
    def __init__(self, user_repository: IUserRepository, password_hasher: IPasswordHasher) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def register(self, email: str, password: str, name: str, role: Role) -> PublicUserData:
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