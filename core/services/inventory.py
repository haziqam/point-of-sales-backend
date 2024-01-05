from typing import List, Optional
from core.models.product import Product
from core.repositories.product import IProductRepository


class InventoryService():
    def __init__(self, product_repository: IProductRepository) -> None:
        self.product_repository = product_repository

    def insert_product(self, name: str, description: str, price: float, stock: int) -> Product:
        return self.product_repository.create_product(name, description, price, stock)

    def find_product_by_id(self, id: str) -> Optional[Product]:
        return self.product_repository.find_product_by_id(id)
    
    def find_products(self, page: int = 1, number_per_page: int = 10, *, name: Optional[str] = None, 
                      description: Optional[str] = None, price: Optional[float] = None, 
                      stock: Optional[int] = None) -> List[Product]:
        return self.product_repository.find_products(
            page, number_per_page, name=name, 
            description=description, price=price, stock=stock)
    
    def update_product(self, product: Product) -> Product:
        return self.product_repository.update_product(product)
    
    def remove_product(self, product: Product) -> None:
        self.product_repository.delete_product(product)
