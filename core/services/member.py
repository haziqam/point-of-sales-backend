from typing import Optional, Tuple
from core.models.member import Member, PublicMemberData, VIPMember
from core.repositories.member import IMemberRepository
from security.hasher import IPasswordHasher
from exceptions.auth_exception import InvalidCredentials, UserNotFound


class MemberService:
    def __init__(
        self, member_repository: IMemberRepository, PIN_hasher: IPasswordHasher
    ) -> None:
        self.member_repository = member_repository
        self.PIN_hasher = PIN_hasher

    def find_member_by_id(self, id: str) -> Optional[Member]:
        return self.member_repository.find_member_by_id(id)

    def register(self, email: str, PIN: str, name: str, **kwargs) -> PublicMemberData:
        hashed_PIN = self.PIN_hasher.hash(PIN)
        new_member = self.member_repository.create_member(
            email, hashed_PIN, name, **kwargs
        )
        return new_member.public_data

    def _login(self, email: str, PIN: str, **kwargs) -> Tuple[PublicMemberData, str]:
        """
        Returns:
            A tuple containing the public member data
            and the member type if authentication is successful.

        Raises:
        * UserNotFound
        * InvalidCredentials
        """
        matching_member = self.member_repository.find_member_by_email(email, **kwargs)
        if matching_member is None:
            raise UserNotFound()

        success = self.PIN_hasher.verify(PIN, matching_member.hashed_PIN)
        if not success:
            raise InvalidCredentials()

        return matching_member.public_data, matching_member.get_member_type()

    def upgrade_to_VIP(self, member: Member) -> Tuple[PublicMemberData, str]:
        vip_member = VIPMember.from_member(member)
        self.member_repository.update_member(vip_member)
        return vip_member.public_data, vip_member.get_member_type()

    def delete_member(self, member: Member) -> None:
        self.member_repository.delete_member(member)
