from pydantic import BaseModel, validator
from core.models.user import PublicUserData, Role
from infrastructure.adapters.rest.utils.validation import (
    validate_email,
    validate_password,
)


class UserRegistrationSchema(BaseModel):
    name: str
    role: Role
    email: str
    password: str

    @validator("email")
    def validate_email(cls, value: str):
        if validate_email(value):
            return value

    @validator("password")
    def validate_password(cls, value: str):
        if validate_password(value):
            return value


class UserLoginSchema(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, value: str):
        if validate_email(value):
            return value

    @validator("password")
    def validate_password(cls, value: str):
        if validate_password(value):
            return value


class UserDataSchema(BaseModel):
    public_data: PublicUserData
    email: str

    @validator("email")
    def validate_email(cls, value: str):
        if validate_email(value):
            return value
