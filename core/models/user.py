from enum import Enum
from pydantic import BaseModel
class Role(Enum):
    CASHIER = 'cashier'
    MANAGER = 'manager'

class PublicUserData(BaseModel):
    id: str
    name: str
    role: Role

class User(BaseModel):
    public_data: PublicUserData
    email: str
    hashed_password: str
