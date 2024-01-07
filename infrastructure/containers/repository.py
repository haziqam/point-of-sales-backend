from core.repositories.bill import IBillRepository
from core.repositories.cash import ICashRepository
from core.repositories.member import IMemberRepository
from core.repositories.product import IProductRepository
from core.repositories.user import IUserRepository


class RepositoryContainer:
    def __init__(
        self,
        bill_repository: IBillRepository,
        cash_repository: ICashRepository,
        member_repository: IMemberRepository,
        product_repository: IProductRepository,
        user_repository: IUserRepository,
    ) -> None:
        self.bill_repository = bill_repository
        self.cash_repository = cash_repository
        self.member_repository = member_repository
        self.product_repository = product_repository
        self.user_repository = user_repository
