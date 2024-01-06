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
from transaction.transaction_provider import ITransactionProvider

TAX_RATE = 0.01
POINT_MULTIPLIER = 0.15


class CashierService:
    def __init__(
        self,
        product_repository: IProductRepository,
        member_repository: IMemberRepository,
        bill_repository: IBillRepository,
        cash_repository: ICashRepository,
        transaction_provider: ITransactionProvider,
    ) -> None:
        self.product_repository = product_repository
        self.member_repository = member_repository
        self.bill_repository = bill_repository
        self.cash_repository = cash_repository
        self.transaction_provider = transaction_provider

    def _process_products(
        self, products_to_purchase: List[Tuple[Product, int]], **kwargs
    ) -> List[PurchasedProduct]:
        purchased_products: List[PurchasedProduct] = []
        for product, amount in products_to_purchase:
            if product.stock < amount:
                raise InsufficientStock()

            product.stock -= amount
            self.product_repository.update_product(product, **kwargs)
            purchased_products.append(
                PurchasedProduct.create_from_product(product, amount)
            )

        return purchased_products

    def _calculate_subtotal_price(
        self, purchased_products: List[PurchasedProduct]
    ) -> float:
        subtotal_price = 0.0
        for product in purchased_products:
            subtotal_price += product.price * product.amount
        return subtotal_price

    def _calculate_reduced_price(
        self, member: Member, subtotal_price: float, points_used: float
    ) -> float:
        return member.convert_price(subtotal_price, points_used)

    def _calculate_taxed_price(self, subtotal_price: float) -> float:
        return subtotal_price * (1 + TAX_RATE)

    def _get_discount_amount(self, member: Member) -> float:
        if member.get_member_type == "VIP Member":
            return cast(VIPMember, member).discount_rate
        return 0.0

    def _processs_member_data(
        self, member: Member, points_used: float, subtotal_price: float, **kwargs
    ) -> None:
        if member.public_data.points < points_used:
            raise InsufficientPoint()

        if points_used > 0.0:
            member.public_data.points -= points_used
        else:
            member.public_data.points += subtotal_price * POINT_MULTIPLIER

        self.member_repository.update_member(member, **kwargs)

    def _purchase(
        self,
        products_to_purchase: List[Tuple[Product, int]],
        member: Optional[Member],
        points_used: float = 0.0,
        **kwargs
    ) -> Bill:
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
        purchased_products = self._process_products(products_to_purchase)
        subtotal_price = self._calculate_subtotal_price(purchased_products)
        discount = 0.0

        if member is not None:
            subtotal_price = self._calculate_reduced_price(
                member, subtotal_price, points_used
            )
            discount = self._get_discount_amount(member)
            self._processs_member_data(member, points_used, subtotal_price)

        total_price = self._calculate_taxed_price(subtotal_price)
        self.cash_repository.add_cash(total_price, **kwargs)

        bill = self.bill_repository.create_bill(
            str(datetime.now()),
            purchased_products,
            subtotal_price,
            total_price,
            points_used,
            discount,
            **kwargs
        )

        return bill

    def purchase(
        self,
        products_to_purchase: List[Tuple[Product, int]],
        member: Optional[Member],
        points_used: float = 0.0,
    ) -> Bill:
        callback = lambda **kwargs: self._purchase(
            products_to_purchase, member, points_used, **kwargs
        )
        return self.transaction_provider.transact(callback)
