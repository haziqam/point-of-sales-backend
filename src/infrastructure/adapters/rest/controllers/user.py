from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response
from core.models.user import PublicUserData
from core.services.user import UserService
from infrastructure.adapters.rest.middlewares.manager_auth import (
    manager_auth_middleware,
)
from infrastructure.adapters.rest.schemas.response_message import ResponseMessageSchema
from infrastructure.adapters.rest.utils.jwt_utils import encode_jwt
from infrastructure.adapters.rest.schemas.user import (
    UserLoginSchema,
    UserRegistrationSchema,
)
from exceptions.auth_exception import (
    InvalidCredentials,
    UserAlreadyExists,
    UserNotFound,
)

USER_LOGIN_EXPIRY_TIME = timedelta(hours=2)


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
        async def login(
            schema: UserLoginSchema,
            response: Response,
        ) -> PublicUserData:
            try:
                public_data = self.user_service.login(**schema.dict())
                token_payload = public_data.copy(
                    update={"role": public_data.role.name}
                ).dict()
                token = encode_jwt(token_payload, USER_LOGIN_EXPIRY_TIME)
                response.set_cookie(
                    key="user-jwt",
                    value=token,
                    max_age=int(USER_LOGIN_EXPIRY_TIME.total_seconds()),
                    httponly=True,
                    samesite="strict",
                )
                return public_data
            except UserNotFound:
                raise HTTPException(
                    status_code=401,
                    detail=f"User with email ({schema.email}) not found",
                )
            except InvalidCredentials:
                raise HTTPException(status_code=401, detail=f"Wrong password")

        @self.delete("/", dependencies=[Depends(manager_auth_middleware)])
        async def delete_user(id: str) -> ResponseMessageSchema:
            user = self.user_service.find_user_by_id(id)
            if user is None:
                raise HTTPException(
                    status_code=404, detail=f"User with id {id} not found"
                )

            self.user_service.delete_user(user)
            return ResponseMessageSchema(
                message=f"User with id {id} deleted successfully"
            )
