from datetime import datetime
from typing import List
from core.models.bill import Bill
from core.models.product import PurchasedProduct
from core.models.report import MonthlyReport
from core.repositories.bill import IBillRepository
from infrastructure.adapters.db.mongodb.base_repository import MongoDBRepository


class BillRepository(IBillRepository, MongoDBRepository):
    def create_bill(
        self,
        transaction_date: datetime,
        purchased_products: List[PurchasedProduct],
        subtotal_price: float,
        total_price: float,
        points_used: float = 0.0,
        discount: float = 0.0,
        **kwargs
    ) -> Bill:
        session = kwargs.get("session", None)
        result = self.collection.insert_one(
            {
                "transaction_date": transaction_date,
                "purchased_products": list(map(lambda e: e.dict(), purchased_products)),
                "subtotal_price": subtotal_price,
                "total_price": total_price,
                "points_used": points_used,
                "discount": discount,
            },
            session=session,
        )
        bill = Bill(
            id=str(result.inserted_id),
            transaction_date=transaction_date,
            purchased_products=purchased_products,
            subtotal_price=subtotal_price,
            points_used=points_used,
            discount=discount,
            total_price=total_price,
        )
        return bill

    def get_purchased_products(
        self, start_date: datetime, end_date: datetime, **kwargs
    ) -> List[PurchasedProduct]:
        session = kwargs.get("session", None)
        cursor = self.collection.aggregate(
            [
                {
                    "$match": {
                        "transaction_date": {
                            "$gte": start_date,
                            "$lt": end_date,
                        }
                    }
                },
                {"$unwind": {"path": "$purchased_products"}},
                {
                    "$group": {
                        "_id": "$purchased_products.id",
                        "product": {"$first": "$purchased_products"},
                        "amount_purchased": {"$sum": "$purchased_products.amount"},
                    }
                },
                {"$unset": ["_id", "product.amount"]},
            ],
            session=session,
        )

        aggregation_result: List[PurchasedProduct] = []
        for doc in cursor:
            doc["amount"] = doc.pop("amount_purchased")
            aggregation_result.append(
                PurchasedProduct(**doc["product"], amount=doc["amount"])
            )

        return aggregation_result

    def get_total_transactions(
        self, start_date: datetime, end_date: datetime, **kwargs
    ) -> int:
        session = kwargs.get("session", None)
        return len(
            self.collection.distinct(
                key="_id",
                filter={
                    "transaction_date": {
                        "$gte": start_date,
                        "$lt": end_date,
                    }
                },
                session=session,
            )
        )

    def get_total_revenue(
        self, start_date: datetime, end_date: datetime, **kwargs
    ) -> float:
        session = kwargs.get("session", None)
        cursor = self.collection.aggregate(
            [
                {
                    "$match": {
                        "transaction_date": {
                            "$gte": start_date,
                            "$lt": end_date,
                        }
                    }
                },
                {"$group": {"_id": None, "total_revenue": {"$sum": "$total_price"}}},
                {"$unset": "_id"},
            ],
            session=session,
        )

        total_revenue = 0.0
        for doc in cursor:
            total_revenue = doc["total_revenue"]

        return total_revenue

    def get_monthly_transactions(self, year: int, **kwargs) -> List[MonthlyReport[int]]:
        session = kwargs.get("session", None)
        cursor = self.collection.aggregate(
            [
                {
                    "$match": {
                        "transaction_date": {
                            "$gte": datetime(year=year, month=1, day=1),
                            "$lt": datetime(year=year, month=12, day=1),
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {"$month": "$transaction_date"},
                        "transactions": {"$count": {}},
                    }
                },
                {"$project": {"month": "$_id", "transactions": 1, "_id": 0}},
            ],
            session=session,
        )

        aggregation_result: List[MonthlyReport[int]] = []
        for doc in cursor:
            aggregation_result.append(
                MonthlyReport[int](
                    month=doc["month"],
                    data=doc["transactions"],
                    data_name="transactions",
                )
            )

        return aggregation_result

    def get_monthly_sold_products(
        self, year: int, **kwargs
    ) -> List[MonthlyReport[int]]:
        session = kwargs.get("session", None)
        cursor = self.collection.aggregate(
            [
                {
                    "$match": {
                        "transaction_date": {
                            "$gte": datetime(year=year, month=1, day=1),
                            "$lt": datetime(year=year, month=12, day=1),
                        }
                    }
                },
                {"$unwind": {"path": "$purchased_products"}},
                {
                    "$group": {
                        "_id": {"$month": "$transaction_date"},
                        "total_purchased_products": {
                            "$sum": "$purchased_products.amount"
                        },
                    }
                },
                {
                    "$project": {
                        "month": "$_id",
                        "_id": 0,
                        "total_purchased_products": 1,
                    }
                },
            ],
            session=session,
        )

        aggregation_result: List[MonthlyReport[int]] = []
        for doc in cursor:
            aggregation_result.append(
                MonthlyReport[int](
                    month=doc["month"],
                    data=doc["total_purchased_products"],
                    data_name="total_purchased_products",
                )
            )

        return aggregation_result
