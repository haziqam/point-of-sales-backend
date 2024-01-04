from abc import ABC, abstractmethod
from typing import Optional, List

from core.models.product import Product

class IProductRepository(ABC):
    @abstractmethod
    def create_product(id: str, name: str, description: str, price: float, stock: int) -> Product:
        pass

    @abstractmethod
    def find_product_by_id(id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def find_products(page: int = 1, number_per_page: int = 10, *, name: str, description: str, price: float, stock: int) -> List[Product]:
        pass

    @abstractmethod
    def update_product(product: Product) -> Product:
        pass

    @abstractmethod
    def delete_product(product: Product) -> None:
        pass