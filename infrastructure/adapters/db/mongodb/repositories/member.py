from typing import Dict, Optional, cast
from bson.objectid import ObjectId
from infrastructure.adapters.db.mongodb.base_repository import MongoDBRepository
from core.models.member import Member, PublicMemberData, VIPMember
from core.repositories.member import IMemberRepository


class MemberRepository(IMemberRepository, MongoDBRepository):
    def create_member(
        self, email: str, hashed_PIN: str, name: str, points: float = 0.0, **kwargs
    ) -> Member:
        session = kwargs.get("session", None)
        result = self.collection.insert_one(
            {
                "public_data": {"name": name, "points": points},
                "email": email,
                "hashed_PIN": hashed_PIN,
                "type": "Member",
            },
            session=session,
        )
        id = str(result.inserted_id)
        public_data = PublicMemberData(id=id, name=name, points=points)
        new_member = Member(public_data=public_data, email=email, hashed_PIN=hashed_PIN)
        return new_member

    def find_member_by_id(self, id: str, **kwargs) -> Optional[Member]:
        session = kwargs.get("session", None)
        result = self.collection.find_one({"_id": ObjectId(id)}, session=session)
        if result is None:
            return None

        result["public_data"]["id"] = str(result.pop("_id"))
        found_member = Member(**result)

        if result["type"] == "VIP Member":
            return VIPMember.from_member(
                found_member, discount_rate=result["discount_rate"]
            )
        return found_member

    def find_member_by_email(self, email: str, **kwargs) -> Optional[Member]:
        session = kwargs.get("session", None)
        result = self.collection.find_one({"email": email}, session=session)
        if result is None:
            return None

        result["public_data"]["id"] = str(result.pop("_id"))
        found_member = Member(**result)

        if result["type"] == "VIP Member":
            return VIPMember.from_member(
                found_member, discount_rate=result["discount_rate"]
            )
        return found_member

    def update_member(self, member: Member, **kwargs) -> Member:
        session = kwargs.get("session", None)
        set_dict = member.dict()
        set_dict["public_data"].pop("id", None)
        set_dict["type"] = member.get_member_type()
        unset_dict = {}
        if member.get_member_type() != "VIP Member":
            unset_dict["discount_rate"] = 1

        self.collection.update_one(
            {"_id": ObjectId(member.public_data.id)},
            {"$set": set_dict, "$unset": unset_dict},
            session=session,
        )
        return member

    def delete_member(self, member: Member, **kwargs) -> None:
        session = kwargs.get("session", None)
        self.collection.delete_one(
            {"_id": ObjectId(member.public_data.id)}, session=session
        )

    def get_member_amount_by_type(self, **kwargs) -> Dict[str, int]:
        """
        Returns:
            A dictionary with member type as the key and amount as the value
        """
        session = kwargs.get("session", None)
        cursor = self.collection.aggregate(
            [
                {"$group": {"_id": "$type", "amount": {"$count": {}}}},
                {"$set": {"type": "$_id"}},
                {"$unset": ["_id"]},
            ],
            session=session,
        )

        aggregation_result: Dict[str, int] = {}
        for doc in cursor:
            aggregation_result[doc["type"]] = doc["amount"]

        return aggregation_result
