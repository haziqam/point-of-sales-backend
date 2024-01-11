import os
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from core.models.product import Product
from core.services.inventory import InventoryService
from infrastructure.adapters.rest.middlewares.manager_auth import (
    manager_auth_middleware,
)
from infrastructure.adapters.rest.middlewares.cashier_manager_auth import (
    cashier_or_manager_auth_middleware,
)
from infrastructure.adapters.rest.schemas.product import (
    ProductSchema,
    UpdateProductSchema,
)
from infrastructure.adapters.rest.utils.file_writer import delete_file, write_file

PRODUCT_IMAGE_PATH = "static/product/images"


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
        async def insert_product(
            request: Request,
            name: str = Form(...),
            description: str = Form(...),
            price: float = Form(...),
            stock: int = Form(...),
            image: UploadFile = File(...),
        ) -> Product:
            try:
                schema = ProductSchema(
                    name=name, description=description, price=price, stock=stock
                )
                product = self.inventory_service.insert_product(**schema.dict())
                if image.filename is not None:
                    ext = os.path.splitext(image.filename)[1]
                    write_file(image, f"{PRODUCT_IMAGE_PATH}/{product.id}{ext}")

                return product
            except ValueError as e:
                raise HTTPException(status_code=422, detail=str(e))

        @self.get("/{id}", dependencies=[Depends(cashier_or_manager_auth_middleware)])
        async def find_product_by_id(id: str) -> Product:
            return self._check_product_id(id)

        @self.get("/", dependencies=[Depends(cashier_or_manager_auth_middleware)])
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
            id: str,
            request: Request,
            name: Optional[str] = Form(None),
            description: Optional[str] = Form(None),
            price: Optional[float] = Form(None),
            stock: Optional[int] = Form(None),
            image: Optional[UploadFile] = None,
        ) -> Product:
            product = self._check_product_id(id)

            try:
                schema = UpdateProductSchema(
                    name=name, description=description, price=price, stock=stock
                )
                if name is not None:
                    product.name = name
                if description is not None:
                    product.description = description
                if price is not None:
                    product.price = price
                if stock is not None:
                    product.stock = stock

                product = self.inventory_service.update_product(product)

                if image is not None and image.filename is not None:
                    delete_file(f"{PRODUCT_IMAGE_PATH}/{product.id}")
                    ext = os.path.splitext(image.filename)[1]
                    write_file(image, f"{PRODUCT_IMAGE_PATH}/{product.id}{ext}")

                return product
            except ValueError as e:
                raise HTTPException(status_code=422, detail=str(e))

        @self.delete("/{id}", dependencies=[Depends(manager_auth_middleware)])
        async def remove_product(id: str, request: Request) -> Dict[str, str]:
            product = self.inventory_service.find_product_by_id(id)
            if product is None:
                raise HTTPException(
                    status_code=404, detail=f"Product with id {id} not available"
                )
            delete_file(f"{PRODUCT_IMAGE_PATH}/{id}")
            self.inventory_service.remove_product(product)
            return {"message": f"Product with id {id} removed successfully"}
