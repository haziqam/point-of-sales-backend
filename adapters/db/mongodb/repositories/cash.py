from typing import cast
from pymongo.collection import Collection
from adapters.db.mongodb.base_repository import MongoDBRepository
from core.repositories.cash import ICashRepository


class CashRepository(ICashRepository, MongoDBRepository):
    def get_cash(self, **kwargs) -> float:
        result = self.collection.find_one()
        if result is not None:
            return cast(float, result["cash"])
        return 0.0

    def add_cash(self, amount: float, **kwargs) -> None:
        current_cash = self.get_cash()
        self.collection.update_one(
            {}, {"$set": {"cash": current_cash + amount}}, upsert=True
        )

    def subtract_cash(self, amount: float, **kwargs) -> None:
        current_cash = self.get_cash()
        self.collection.update_one(
            {}, {"$set": {"cash": current_cash - amount}}, upsert=True
        )

    def is_sufficient(self, amount: float, **kwargs) -> bool:
        current_cash = self.get_cash()
        return current_cash >= amount
