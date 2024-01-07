from typing import Optional

from bson import ObjectId
from infrastructure.adapters.db.mongodb.base_repository import MongoDBRepository
from core.models.user import PublicUserData, Role, User
from core.repositories.user import IUserRepository


class UserRepository(IUserRepository, MongoDBRepository):
    def create_user(
        self, name: str, role: Role, email: str, hashed_password: str, **kwargs
    ) -> User:
        result = self.collection.insert_one(
            {
                "public_data": {"name": name, "role": role.value},
                "email": email,
                "hashed_password": hashed_password,
            },
        )
        id = str(result.inserted_id)
        public_data = PublicUserData(id=id, name=name, role=role)
        new_user = User(
            public_data=public_data, email=email, hashed_password=hashed_password
        )
        return new_user

    def find_user_by_id(self, id: str, **kwargs) -> Optional[User]:
        result = self.collection.find_one({"_id": ObjectId(id)})
        if result is None:
            return None

        result["public_data"]["id"] = str(result.pop("_id"))
        found_user = User(**result)
        return found_user

    def find_user_by_email(self, email: str, **kwargs) -> Optional[User]:
        result = self.collection.find_one({"email": email})
        if result is None:
            return None

        result["public_data"]["id"] = str(result.pop("_id"))
        found_user = User(**result)
        return found_user

    def update_user(self, user: User, **kwargs) -> User:
        set_dict = user.dict()
        set_dict["public_data"].pop("id")
        self.collection.update_one(
            {"_id": ObjectId(user.public_data.id)}, {"$set": set_dict}
        )
        return user

    def delete_user(self, user: User, **kwargs) -> None:
        self.collection.delete_one({"_id": ObjectId(user.public_data.id)})
