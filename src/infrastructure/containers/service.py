from core.services.cashier import CashierService
from core.services.inventory import InventoryService
from core.services.member import MemberService
from core.services.report import ReportService
from core.services.user import UserService


class ServiceContainer:
    def __init__(
        self,
        cashier_service: CashierService,
        inventory_service: InventoryService,
        member_service: MemberService,
        report_service: ReportService,
        user_service: UserService,
    ) -> None:
        self.cashier_service = cashier_service
        self.inventory_service = inventory_service
        self.member_service = member_service
        self.report_service = report_service
        self.user_service = user_service
