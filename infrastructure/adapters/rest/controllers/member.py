from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response
from core.models.member import Member, PublicMemberData
from core.services.member import MemberService
from infrastructure.adapters.rest.schemas.response_message import ResponseMessageSchema
from infrastructure.adapters.rest.schemas.member import (
    MemberDataSchema,
    MemberLoginSchema,
    MemberRegistrationSchema,
)
from infrastructure.adapters.rest.utils.jwt_utils import encode_jwt
from infrastructure.adapters.rest.middlewares.cashier_auth import (
    cashier_auth_middleware,
)
from infrastructure.adapters.rest.middlewares.member_auth import member_auth_middleware
from exceptions.auth_exception import (
    InvalidCredentials,
    UserAlreadyExists,
    UserNotFound,
)

MEMBER_LOGIN_EXPIRY_TIME = timedelta(minutes=5)


class MemberController(APIRouter):
    def __init__(self, member_service: MemberService) -> None:
        super().__init__(prefix="/members")
        self.member_service = member_service
        self._assign_routes()

    def _check_member_id(self, id: str) -> Member:
        member = self.member_service.find_member_by_id(id)
        if member is None:
            raise HTTPException(
                status_code=404, detail=f"Member with id {id} not found"
            )
        return member

    def _assign_routes(self):
        @self.post(
            "/",
            dependencies=[
                Depends(cashier_auth_middleware),
                Depends(member_auth_middleware),
            ],
        )
        async def register(schema: MemberRegistrationSchema) -> PublicMemberData:
            try:
                return self.member_service.register(**schema.dict())
            except UserAlreadyExists:
                raise HTTPException(
                    status_code=400,
                    detail=f"Member with this email ({schema.email}) already registered",
                )

        @self.delete(
            "/{id}",
            dependencies=[
                Depends(cashier_auth_middleware),
                Depends(member_auth_middleware),
            ],
        )
        async def delete_member(id: str) -> ResponseMessageSchema:
            member = self._check_member_id(id)
            self.member_service.delete_member(member)
            return ResponseMessageSchema(
                message=f"Member with id {id} deleted successfully"
            )

        @self.put("/session")
        async def login(
            schema: MemberLoginSchema, response: Response
        ) -> MemberDataSchema:
            try:
                public_data, member_type = self.member_service.login(**schema.dict())
                token = encode_jwt(public_data.dict(), MEMBER_LOGIN_EXPIRY_TIME)
                response.set_cookie(
                    key="member-jwt",
                    value=token,
                    max_age=int(MEMBER_LOGIN_EXPIRY_TIME.total_seconds()),
                    httponly=True,
                    samesite="strict",
                )
                return MemberDataSchema(
                    public_data=public_data, member_type=member_type
                )
            except UserNotFound:
                raise HTTPException(
                    status_code=401, detail=f"User with email {schema.email} not found"
                )
            except InvalidCredentials:
                raise HTTPException(status_code=401, detail="Wrong password")

        @self.put(
            "/{id}/vip-subscription",
            dependencies=[
                Depends(cashier_auth_middleware),
                Depends(member_auth_middleware),
            ],
        )
        async def upgrade_to_VIP(id: str) -> MemberDataSchema:
            member = self._check_member_id(id)
            public_data, member_type = self.member_service.upgrade_to_VIP(member)
            return MemberDataSchema(public_data=public_data, member_type=member_type)

        @self.delete(
            "/{id}/vip-subscription",
            dependencies=[
                Depends(cashier_auth_middleware),
                Depends(member_auth_middleware),
            ],
        )
        async def cancel_VIP(id: str) -> MemberDataSchema:
            member = self._check_member_id(id)
            public_data, member_type = self.member_service.cancel_VIP(member)
            return MemberDataSchema(public_data=public_data, member_type=member_type)
