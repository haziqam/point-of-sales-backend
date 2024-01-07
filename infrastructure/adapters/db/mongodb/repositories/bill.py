from typing import List
from infrastructure.adapters.db.mongodb.base_repository import MongoDBRepository
from core.models.bill import Bill
from core.models.product import PurchasedProduct
from core.repositories.bill import IBillRepository


class BillRepository(IBillRepository, MongoDBRepository):
    def create_bill(
        self,
        transaction_date: str,
        purchased_products: List[PurchasedProduct],
        subtotal_price: float,
        total_price: float,
        points_used: float = 0.0,
        discount: float = 0.0,
        **kwargs
    ) -> Bill:
        result = self.collection.insert_one(
            {
                "transaction_date": transaction_date,
                "purchased_products": list(map(lambda e: e.dict(), purchased_products)),
                "subtotal_price": subtotal_price,
                "total_price": total_price,
                "points_used": points_used,
                "discount": discount,
            }
        )
        bill = Bill(
            id=result.inserted_id,
            transaction_date=transaction_date,
            purchased_products=purchased_products,
            subtotal_price=subtotal_price,
            points_used=points_used,
            discount=discount,
            total_price=total_price,
        )
        return bill
