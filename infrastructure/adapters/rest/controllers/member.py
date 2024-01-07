from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.models.member import Member, PublicMemberData
from core.services.member import MemberService
from exceptions.auth_exception import (
    InvalidCredentials,
    UserAlreadyExists,
    UserNotFound,
)


class MemberRegistrationSchema(BaseModel):
    email: str
    PIN: str
    name: str


class MemberLoginSchema(BaseModel):
    email: str
    PIN: str


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
        async def delete_member(id: str) -> Dict[str, str]:
            member = self._check_member_id(id)
            self.member_service.delete_member(member)
            return {"message": f"Member with id {id} deleted successfully"}

        @self.put("/session")
        async def login(schema: MemberLoginSchema) -> Dict[str, Any]:
            try:
                public_data, member_type = self.member_service.login(**schema.dict())
                return {"public_data": public_data, "member_type": member_type}
            except UserNotFound:
                raise HTTPException(
                    status_code=404, detail=f"User with email {schema.email} not found"
                )
            except InvalidCredentials:
                raise HTTPException(status_code=404, detail="Wrong password")

        @self.put("/{id}/VIP-subscription")
        async def upgrade_to_VIP(id: str) -> Dict[str, Any]:
            member = self._check_member_id(id)
            public_data, member_type = self.member_service.upgrade_to_VIP(member)
            return {"public_data": public_data, "member_type": member_type}

        @self.delete("/{id}/VIP-subscription")
        async def cancel_VIP(id: str) -> Dict[str, Any]:
            member = self._check_member_id(id)
            public_data, member_type = self.member_service.cancel_VIP(member)
            return {"public_data": public_data, "member_type": member_type}
