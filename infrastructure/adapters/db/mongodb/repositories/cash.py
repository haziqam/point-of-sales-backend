from typing import cast
from pymongo.collection import Collection
from infrastructure.adapters.db.mongodb.base_repository import MongoDBRepository
from core.repositories.cash import ICashRepository


class CashRepository(ICashRepository, MongoDBRepository):
    def get_cash(self, **kwargs) -> float:
        session = kwargs.get("session", None)
        result = self.collection.find_one(session=session)
        if result is not None:
            return cast(float, result["cash"])
        return 0.0

    def add_cash(self, amount: float, **kwargs) -> None:
        session = kwargs.get("session", None)
        current_cash = self.get_cash(**kwargs)
        self.collection.update_one(
            {}, {"$set": {"cash": current_cash + amount}}, upsert=True, session=session
        )

    def subtract_cash(self, amount: float, **kwargs) -> None:
        session = kwargs.get("session", None)
        current_cash = self.get_cash(**kwargs)
        self.collection.update_one(
            {}, {"$set": {"cash": current_cash - amount}}, upsert=True, session=session
        )

    def is_sufficient(self, amount: float, **kwargs) -> bool:
        session = kwargs.get("session", None)
        current_cash = self.get_cash(**kwargs)
        return current_cash >= amount
