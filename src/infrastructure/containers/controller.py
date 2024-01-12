from infrastructure.adapters.rest.controllers.cashier import CashierController
from infrastructure.adapters.rest.controllers.member import MemberController
from infrastructure.adapters.rest.controllers.product import ProductController
from infrastructure.adapters.rest.controllers.report import ReportController
from infrastructure.adapters.rest.controllers.user import UserController


class ControllerContainer:
    def __init__(
        self,
        cahsier_controller: CashierController,
        member_controller: MemberController,
        product_controller: ProductController,
        report_controller: ReportController,
        user_controller: UserController,
    ) -> None:
        self.cahsier_controller = cahsier_controller
        self.member_controller = member_controller
        self.product_controller = product_controller
        self.report_controller = report_controller
        self.user_controller = user_controller
