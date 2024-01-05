from abc import ABC, abstractmethod
from typing import Optional, List

from core.models.product import Product

class IProductRepository(ABC):
    @abstractmethod
    def create_product(self, name: str, description: str, price: float, stock: int) -> Product:
        pass

    @abstractmethod
    def find_product_by_id(self, id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def find_products(self, page: int = 1, number_per_page: int = 10, *, 
                      name: Optional[str] = None, description: Optional[str] = None, 
                      price: Optional[float] = None, stock: Optional[int] = None) -> List[Product]:
        pass

    @abstractmethod
    def update_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def delete_product(self, product: Product) -> None:
        pass