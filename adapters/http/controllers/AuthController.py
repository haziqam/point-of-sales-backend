from fastapi import APIRouter
from pydantic import BaseModel, validator

class PublicUserData(BaseModel):
    id: int
    role: str

class User(BaseModel):
    public_data: PublicUserData
    hashed_password: str

# just an example
userData = PublicUserData(id=10, role="Manager")
user = User(public_data=userData, hashed_password="ajuq83920v")

class UserCredentials(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, value):
        # Custom email validation logic
        if not value.endswith("@example.com"):
            raise ValueError("Only email addresses from example.com are allowed")
        return value

class AuthService:
    def __init__(self, a) -> None:
        self.a = a

    def printa(self):
        print(self.a)

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class AuthController(APIRouter, metaclass=SingletonMeta):
    def __init__(self, auth_service: AuthService) -> None:
        super().__init__(prefix="/auth")
        self.auth_service = auth_service
        
    def set_auth_service(self, auth_service: AuthService):
        self.auth_service = auth_service

auth_controller = AuthController(auth_service=None)

@auth_controller.post("/register")
async def register(credentials: UserCredentials):
    auth_controller.auth_service.printa()
    return user.public_data

@auth_controller.get("/login")
async def login():
    auth_controller.auth_service.printa()
    return user.public_data
