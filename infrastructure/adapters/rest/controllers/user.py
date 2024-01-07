from typing import Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.models.user import PublicUserData, Role
from core.services.user import UserService
from exceptions.auth_exception import (
    InvalidCredentials,
    UserAlreadyExists,
    UserNotFound,
)


class UserRegistrationSchema(BaseModel):
    name: str
    role: Role
    email: str
    password: str


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserController(APIRouter):
    def __init__(self, user_service: UserService) -> None:
        super().__init__(prefix="/users")
        self.user_service = user_service
        self._assign_routes()

    def _assign_routes(self):
        @self.post("/")
        async def register(schema: UserRegistrationSchema) -> PublicUserData:
            try:
                return self.user_service.register(**schema.dict())
            except UserAlreadyExists:
                raise HTTPException(
                    status_code=400,
                    detail=f"User with this email ({schema.email}) already registered",
                )

        @self.put("/session")
        async def login(schema: UserLoginSchema) -> PublicUserData:
            try:
                return self.user_service.login(**schema.dict())
            except UserNotFound:
                raise HTTPException(
                    status_code=404,
                    detail=f"User with email ({schema.email}) not found",
                )
            except InvalidCredentials:
                raise HTTPException(status_code=400, detail=f"Wrong password")

        @self.delete("/")
        async def delete_user(id: str) -> Dict[str, str]:
            user = self.user_service.find_user_by_id(id)
            if user is None:
                raise HTTPException(
                    status_code=404, detail=f"User with id {id} not found"
                )

            self.user_service.delete_user(user)
            return {"message": f"User with id {id} deleted successfully"}
