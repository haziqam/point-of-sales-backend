from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from core.models.product import Product
from core.services.inventory import InventoryService
from infrastructure.adapters.rest.middlewares.manager_auth import (
    manager_auth_middleware,
)
from infrastructure.adapters.rest.schemas.product import (
    ProductSchema,
    UpdateProductSchema,
)


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
        @self.post("/", dependencies=[Depends(manager_auth_middleware)])
        async def insert_product(schema: ProductSchema, request: Request) -> Product:
            return self.inventory_service.insert_product(**schema.dict())

        @self.get("/{id}", dependencies=[Depends(manager_auth_middleware)])
        async def find_product_by_id(id: str) -> Product:
            return self._check_product_id(id)

        @self.get("/", dependencies=[Depends(manager_auth_middleware)])
        async def find_products(
            request: Request,
            name: Optional[str] = None,
            description: Optional[str] = None,
            price: Optional[float] = None,
            stock: Optional[int] = None,
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

        @self.patch("/{id}", dependencies=[Depends(manager_auth_middleware)])
        async def update_product(
            id: str, schema: UpdateProductSchema, request: Request
        ) -> Product:
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

        @self.delete("/{id}", dependencies=[Depends(manager_auth_middleware)])
        async def remove_product(id: str, request: Request) -> Dict[str, str]:
            product = self.inventory_service.find_product_by_id(id)
            if product is None:
                raise HTTPException(
                    status_code=404, detail=f"Product with id {id} not available"
                )
            self.inventory_service.remove_product(product)
            return {"message": f"Product with id {id} removed successfully"}
