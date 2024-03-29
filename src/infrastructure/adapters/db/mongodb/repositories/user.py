from typing import Optional, List
from pymongo.cursor import Cursor
from bson import ObjectId
from infrastructure.adapters.db.mongodb.base_repository import MongoDBRepository
from core.models.user import PublicUserData, Role, User
from core.repositories.user import IUserRepository


class UserRepository(IUserRepository, MongoDBRepository):
    def create_user(
        self, name: str, role: Role, email: str, hashed_password: str, **kwargs
    ) -> User:
        session = kwargs.get("session", None)
        result = self.collection.insert_one(
            {
                "public_data": {"name": name, "role": role.value},
                "email": email,
                "hashed_password": hashed_password,
            },
            session=session,
        )
        id = str(result.inserted_id)
        public_data = PublicUserData(id=id, name=name, role=role)
        new_user = User(
            public_data=public_data, email=email, hashed_password=hashed_password
        )
        return new_user

    def find_user_by_id(self, id: str, **kwargs) -> Optional[User]:
        session = kwargs.get("session", None)
        result = self.collection.find_one({"_id": ObjectId(id)}, session=session)
        if result is None:
            return None

        result["public_data"]["id"] = str(result.pop("_id"))
        found_user = User(**result)
        return found_user

    def find_user_by_email(self, email: str, **kwargs) -> Optional[User]:
        session = kwargs.get("session", None)
        result = self.collection.find_one({"email": email}, session=session)
        if result is None:
            return None

        result["public_data"]["id"] = str(result.pop("_id"))
        found_user = User(**result)
        return found_user

    def update_user(self, user: User, **kwargs) -> User:
        session = kwargs.get("session", None)
        set_dict = user.dict()
        set_dict["public_data"].pop("id")
        self.collection.update_one(
            {"_id": ObjectId(user.public_data.id)}, {"$set": set_dict}, session=session
        )
        return user

    def delete_user(self, user: User, **kwargs) -> None:
        session = kwargs.get("session", None)
        self.collection.delete_one(
            {"_id": ObjectId(user.public_data.id)}, session=session
        )

    def find_users(
        self,
        page: int = 1,
        number_per_page: int = 10,
        *,
        id: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        role: Optional[Role] = None,
        **kwargs
    ) -> List[User]:
        session = kwargs.get("session", None)
        filter = {}

        if id is not None:
            filter["_id"] = ObjectId(id)
        if name is not None:
            filter["public_data.name"] = {"$regex": name, "$options": "i"}
        if email is not None:
            filter["email"] = {"$regex": email, "$options": "i"}
        if role is not None:
            filter["public_data.role"] = role.value

        cursor: Cursor = (
            self.collection.find(filter, session=session)
            .skip((page - 1) * number_per_page)
            .limit(number_per_page)
        )
        search_result: List[User] = []
        for doc in cursor:
            doc["public_data"]["id"] = str(doc.pop("_id"))
            search_result.append(User(**doc))

        return search_result
