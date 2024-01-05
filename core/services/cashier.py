from datetime import datetime
from typing import List, Optional, Tuple, cast
from core.models.bill import Bill
from core.models.member import Member, VIPMember
from core.models.product import Product, PurchasedProduct
from core.repositories.product import IProductRepository
from core.repositories.member import IMemberRepository
from core.repositories.bill import IBillRepository
from core.repositories.cash import ICashRepository
from exceptions.transaction_exception import InsufficientPoint, InsufficientStock

class CashierService():
    TAX_RATE = 0.01
    def __init__(self, product_repository: IProductRepository, member_repository: IMemberRepository, 
                 bill_repository: IBillRepository, cash_repository: ICashRepository) -> None:
        self.product_repository = product_repository
        self.member_repository = member_repository
        self.bill_repository = bill_repository
        self.cash_repository = cash_repository

    def purchase(self, products_to_purchase: List[Tuple[Product, int]], 
                 member: Optional[Member], points_used: float = 0.0) -> Bill:
        """
            Parameters
            * products_to_purchase: List of tuples containing the product and the amount to purchcase
            * member: the member purchasing the product (if any)
            * points_used: float = points used by the member to reduce the price (if any)
            
            Returns
                bill

            Raises
            * InsufficientStock
            * InsufficientPoint
        """
        # Start transaction
        subtotal_price = 0.0
        purchased_products: List[PurchasedProduct] = []
        for product, amount in products_to_purchase:
            if product.stock < amount:
                raise InsufficientStock() # rollback
            
            subtotal_price += product.price * amount
            product.stock -= amount
            purchased_products.append(PurchasedProduct.create_from_product(product, amount))
            self.product_repository.update_product(product)

        total_price = subtotal_price
        discount = 0.0

        if member is not None:
            if member.public_data.points < points_used:
                raise InsufficientPoint() # rollback
            
            total_price = member.convert_price(subtotal_price, points_used=points_used)

            if member.get_member_type() == 'VIP Member':
                discount = cast(VIPMember, member).discount_rate

        bill = self.bill_repository.create_bill(
            str(datetime.now()), purchased_products, 
            subtotal_price, total_price, points_used, discount)
        
        # Commit transaction
        return bill


        