from fastapi import APIRouter
from pydantic import BaseModel, validator

from utils.singleton import SingletonMeta

class PublicExampleData(BaseModel):
    id: int
    role: str

class ExampleModel(BaseModel):
    public_data: PublicExampleData
    hashed_password: str

# just an example
userData = PublicExampleData(id=10, role="Manager")
user = ExampleModel(public_data=userData, hashed_password="ajuq83920v")

class ExampleCredentialsSchema(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, value):
        # Custom email validation logic
        if not value.endswith("@example.com"):
            raise ValueError("Only email addresses from example.com are allowed")
        return value

class ExampleService:
    def __init__(self, a) -> None:
        self.a = a

    def printa(self):
        print(self.a)

class ExampleController(APIRouter, metaclass=SingletonMeta):
    def __init__(self, example_service: ExampleService) -> None:
        super().__init__(prefix="/exampleAuth")
        self._example_service = example_service
        
    def set_example_service(self, example_service: ExampleService):
        self._example_service = example_service

example_controller = ExampleController(example_service=None)

@example_controller.post("/register")
async def register(credentials: ExampleCredentialsSchema):
    example_controller.example_service.printa()
    return user.public_data

@example_controller.get("/login")
async def login():
    example_controller.example_service.printa()
    return user.public_data
