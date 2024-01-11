from typing import List, Optional, Tuple
from fastapi import APIRouter, Depends, HTTPException, Request
from core.models.bill import Bill
from core.models.product import Product
from core.services.cashier import CashierService
from core.services.inventory import InventoryService
from core.services.member import MemberService
from exceptions.transaction_exception import TransactionException
from infrastructure.adapters.rest.schemas.purchase import (
    PurchaseSchema,
)
from infrastructure.adapters.rest.middlewares.cashier_auth import (
    cashier_auth_middleware,
)
from infrastructure.adapters.rest.middlewares.member_auth import (
    member_payment_auth_middleware,
)


class CashierController(APIRouter):
    def __init__(
        self,
        cashier_service: CashierService,
        inventory_service: InventoryService,
        member_service: MemberService,
    ) -> None:
        super().__init__(prefix="/cashier")
        self.cashier_service = cashier_service
        self.inventory_service = inventory_service
        self.member_service = member_service
        self._assign_routes()

    def _assign_routes(self):
        @self.post(
            "/payment",
            dependencies=[
                Depends(cashier_auth_middleware),
                Depends(member_payment_auth_middleware),
            ],
        )
        async def purchase(schema: PurchaseSchema, request: Request) -> Bill:
            request.cookies.pop("member-jwt", None)
            products_to_purchase: List[Tuple[Product, int]] = []
            for product in schema.products:
                found_product = self.inventory_service.find_product_by_id(product.id)
                if found_product is None:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product with id {product.id} not found",
                    )

                products_to_purchase.append((found_product, product.amount))

            member = None
            points_used = 0.0
            if schema.member_id is not None:
                member = self.member_service.find_member_by_id(schema.member_id)
                if member is None:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Member with id {schema.member_id} not found",
                    )
                if schema.points_used is not None:
                    points_used = schema.points_used

            try:
                bill = self.cashier_service.purchase(
                    products_to_purchase, member, points_used
                )
                return bill
            except TransactionException as e:
                raise HTTPException(
                    status_code=400, detail=f"Unable to complete transaction: {str(e)}"
                )
