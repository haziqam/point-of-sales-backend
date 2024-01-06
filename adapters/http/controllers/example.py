from fastapi import APIRouter
from pydantic import BaseModel, validator


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


class ExampleController(APIRouter):
    def __init__(self, example_service: ExampleService) -> None:
        super().__init__(prefix="/exampleAuth")
        self.example_service = example_service
        self.assign_routes()

    def assign_routes(self) -> None:
        @self.post("/register")
        async def register(credentials: ExampleCredentialsSchema):
            self.example_service.printa()
            return user.public_data

        @self.get("/login")
        async def login():
            self.example_service.printa()
            return user.public_data
