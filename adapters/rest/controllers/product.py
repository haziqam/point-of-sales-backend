from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.models.product import Product
from core.services.inventory import InventoryService


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class UpdateProductSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]


class ProductController(APIRouter):
    def __init__(self, inventory_service: InventoryService):
        super().__init__(prefix="/products")
        self.inventory_service = inventory_service
        self._assign_routes()

    def _check_product_id(self, id: str) -> Product:
        product = self.inventory_service.find_product_by_id(id)
        if product is None:
            raise HTTPException(
                status_code=404, detail=f"Product with id {id} not found"
            )
        return product

    def _assign_routes(self):
        @self.post("/")
        async def insert_product(schema: ProductSchema) -> Product:
            return self.inventory_service.insert_product(**schema.dict())

        @self.get("/{id}")
        async def find_product_by_id(id: str) -> Product:
            return self._check_product_id(id)

        @self.get("/")
        async def find_products(
            name: Optional[str],
            description: Optional[str],
            price: Optional[float],
            stock: Optional[int],
            page: int = 1,
            number_per_page: int = 10,
        ) -> List[Product]:
            return self.inventory_service.find_products(
                page=page,
                number_per_page=number_per_page,
                name=name,
                description=description,
                price=price,
                stock=stock,
            )

        @self.patch("/{id}")
        async def update_product(id: str, schema: UpdateProductSchema) -> Product:
            product = self._check_product_id(id)

            if schema.name is not None:
                product.name = schema.name
            if schema.description is not None:
                product.description = schema.description
            if schema.price is not None:
                product.price = schema.price
            if schema.stock is not None:
                product.stock = schema.stock

            return self.inventory_service.update_product(product)

        @self.delete("/{id}")
        async def remove_product(id: str) -> Dict[str, str]:
            product = self.inventory_service.find_product_by_id(id)
            if product is None:
                raise HTTPException(
                    status_code=404, detail=f"Product with id {id} not available"
                )
            self.inventory_service.remove_product(product)
            return {"message": f"Product with id {id} removed successfully"}
