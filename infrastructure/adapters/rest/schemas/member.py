from pydantic import BaseModel, validator
from core.models.member import PublicMemberData
from infrastructure.adapters.rest.utils.validation import validate_email, validate_PIN


class MemberRegistrationSchema(BaseModel):
    email: str
    PIN: str
    name: str

    @validator("email")
    def validate_email(cls, value: str):
        if validate_email(value):
            return value

    @validator("PIN")
    def validate_password(cls, value: str):
        if validate_PIN(value):
            return value


class MemberLoginSchema(BaseModel):
    email: str
    PIN: str

    @validator("email")
    def validate_email(cls, value: str):
        if validate_email(value):
            return value

    @validator("PIN")
    def validate_password(cls, value: str):
        if validate_PIN(value):
            return value


class MemberDataSchema(BaseModel):
    public_data: PublicMemberData
    member_type: str
