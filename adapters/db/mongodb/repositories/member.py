from typing import Optional
from adapters.db.mongodb.base_repository import MongoDBRepository
from core.models.member import Member, PublicMemberData
from core.repositories.member import IMemberRepository


class MemberRepository(IMemberRepository, MongoDBRepository):
    def create_member(
        self, email: str, hashed_PIN: str, name: str, points: float = 0.0, **kwargs
    ) -> Member:
        session = kwargs.get("session")
        if session is None:
            raise TypeError("Session is required for creating a member.")

        result = self.collection.insert_one(
            {
                "public_data": {"name": name, "points": points},
                "email": email,
                "hashed_PIN": hashed_PIN,
            },
            session=session,
        )

        id = str(result.inserted_id)
        public_data = PublicMemberData(id=id, name=name, points=points)
        new_member = Member(public_data=public_data, email=email, hashed_PIN=hashed_PIN)
        return new_member

    def find_member_by_id(self, id: str, **kwargs) -> Optional[Member]:
        pass

    def find_member_by_email(self, email: str, **kwargs) -> Optional[Member]:
        pass

    def update_member(self, member: Member, **kwargs) -> Member:
        return member

    def delete_member(self, member: Member, **kwargs) -> None:
        pass
