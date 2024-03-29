from typing import Optional, List
from pymongo.cursor import Cursor
from bson import ObjectId
from infrastructure.adapters.db.mongodb.base_repository import MongoDBRepository
from core.models.product import Product
from core.repositories.product import IProductRepository


class ProductRepository(IProductRepository, MongoDBRepository):
    def create_product(
        self, name: str, description: str, price: float, stock: int, **kwargs
    ) -> Product:
        session = kwargs.get("session", None)
        result = self.collection.insert_one(
            {"name": name, "description": description, "price": price, "stock": stock},
            session=session,
        )
        new_product = Product(
            id=str(result.inserted_id),
            name=name,
            description=description,
            price=price,
            stock=stock,
        )
        return new_product

    def find_product_by_id(self, id: str, **kwargs) -> Optional[Product]:
        session = kwargs.get("session", None)
        result = self.collection.find_one({"_id": ObjectId(id)}, session=session)
        if result is None:
            return None

        result["id"] = str(result.pop("_id"))
        return Product(**result)

    def find_products(
        self,
        page: int = 1,
        number_per_page: int = 10,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        stock: Optional[int] = None,
        **kwargs
    ) -> List[Product]:
        session = kwargs.get("session", None)
        filter = {}

        if name is not None:
            filter["name"] = {"$regex": name, "$options": "i"}
        if description is not None:
            filter["description"] = {"$regex": description, "$options": "i"}
        if price is not None:
            filter["price"] = price
        if stock is not None:
            filter["stock"] = stock

        cursor: Cursor = (
            self.collection.find(filter, session=session)
            .skip((page - 1) * number_per_page)
            .limit(number_per_page)
        )
        search_result: List[Product] = []
        for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            search_result.append(Product(**doc))

        return search_result

    def update_product(self, product: Product, **kwargs) -> Product:
        session = kwargs.get("session", None)
        set_dict = product.dict()
        set_dict.pop("id", None)
        self.collection.update_one(
            {"_id": ObjectId(product.id)}, {"$set": set_dict}, session=session
        )
        return product

    def delete_product(self, product: Product, **kwargs) -> None:
        session = kwargs.get("session", None)
        self.collection.delete_one({"_id": ObjectId(product.id)}, session=session)
