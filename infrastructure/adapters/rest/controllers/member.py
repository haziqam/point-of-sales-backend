from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from adapters.rest.schemas.response_message import ResponseMessageSchema
from core.models.member import Member, PublicMemberData
from core.services.member import MemberService
from infrastructure.adapters.rest.schemas.member import (
    MemberDataSchema,
    MemberLoginSchema,
    MemberRegistrationSchema,
)
from exceptions.auth_exception import (
    InvalidCredentials,
    UserAlreadyExists,
    UserNotFound,
)


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
        @self.post("/")
        async def register(schema: MemberRegistrationSchema) -> PublicMemberData:
            try:
                return self.member_service.register(**schema.dict())
            except UserAlreadyExists:
                raise HTTPException(
                    status_code=400,
                    detail=f"Member with this email ({schema.email}) already registered",
                )

        @self.delete("/{id}")
        async def delete_member(id: str) -> ResponseMessageSchema:
            member = self._check_member_id(id)
            self.member_service.delete_member(member)
            return ResponseMessageSchema(
                message=f"Member with id {id} deleted successfully"
            )

        @self.put("/session")
        async def login(schema: MemberLoginSchema) -> MemberDataSchema:
            try:
                public_data, member_type = self.member_service.login(**schema.dict())
                return MemberDataSchema(
                    public_data=public_data, member_type=member_type
                )
            except UserNotFound:
                raise HTTPException(
                    status_code=404, detail=f"User with email {schema.email} not found"
                )
            except InvalidCredentials:
                raise HTTPException(status_code=404, detail="Wrong password")

        @self.put("/{id}/vip-subscription")
        async def upgrade_to_VIP(id: str) -> MemberDataSchema:
            member = self._check_member_id(id)
            public_data, member_type = self.member_service.upgrade_to_VIP(member)
            return MemberDataSchema(public_data=public_data, member_type=member_type)

        @self.delete("/{id}/vip-subscription")
        async def cancel_VIP(id: str) -> MemberDataSchema:
            member = self._check_member_id(id)
            public_data, member_type = self.member_service.cancel_VIP(member)
            return MemberDataSchema(public_data=public_data, member_type=member_type)
