import os
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from infrastructure.adapters.db.mongodb.repositories.cash import CashRepository
from infrastructure.adapters.db.mongodb.repositories.member import MemberRepository
from infrastructure.adapters.db.mongodb.repositories.product import ProductRepository
from infrastructure.adapters.db.mongodb.repositories.user import UserRepository
from infrastructure.adapters.db.mongodb.repositories.bill import BillRepository
from infrastructure.adapters.db.mongodb.transaction_provider import (
    MongoDBTransactionProvider,
)
from infrastructure.adapters.rest.controllers.cashier import CashierController
from infrastructure.adapters.rest.controllers.member import MemberController
from infrastructure.adapters.rest.controllers.product import ProductController
from infrastructure.adapters.rest.controllers.report import ReportController
from infrastructure.adapters.rest.controllers.user import UserController
from infrastructure.containers.controller import ControllerContainer
from infrastructure.containers.repository import RepositoryContainer
from infrastructure.containers.security import SecurityContainer
from infrastructure.containers.service import ServiceContainer
from infrastructure.containers.transaction import TransactionContainer
from infrastructure.containers.db import DbContainer
from core.services.cashier import CashierService
from core.services.inventory import InventoryService
from core.services.member import MemberService
from core.services.report import ReportService
from core.services.user import UserService
from security.bcrypt.hasher import BCryptPasswordHasher

load_dotenv()


def include_documentation(app: FastAPI) -> None:
    @app.get(app.root_path + "/openapi.json")
    def custom_swagger_ui_html():
        return app.openapi()


def start_app() -> FastAPI:
    db_container = DbContainer(
        MongoClient(
            os.getenv("CONN_STRING", "mongodb://localhost:27017/?replicaSet=rs0")
        )
    )

    repository_container = RepositoryContainer(
        BillRepository(db_container.db.bill),
        CashRepository(db_container.db.cash),
        MemberRepository(db_container.db.member),
        ProductRepository(db_container.db.product),
        UserRepository(db_container.db.user),
    )

    transaction_container = TransactionContainer(
        MongoDBTransactionProvider(db_container.client)
    )

    security_container = SecurityContainer(
        BCryptPasswordHasher(),
    )

    service_container = ServiceContainer(
        CashierService(
            repository_container.product_repository,
            repository_container.member_repository,
            repository_container.bill_repository,
            repository_container.cash_repository,
            transaction_container.transaction_provider,
        ),
        InventoryService(
            repository_container.product_repository,
        ),
        MemberService(
            repository_container.member_repository, security_container.hasher
        ),
        ReportService(
            repository_container.product_repository,
            repository_container.bill_repository,
            transaction_container.transaction_provider,
        ),
        UserService(
            repository_container.user_repository,
            security_container.hasher,
        ),
    )

    controller_container = ControllerContainer(
        CashierController(
            service_container.cashier_service,
            service_container.inventory_service,
            service_container.member_service,
        ),
        MemberController(
            service_container.member_service,
        ),
        ProductController(
            service_container.inventory_service,
        ),
        ReportController(
            service_container.report_service,
        ),
        UserController(
            service_container.user_service,
        ),
    )

    app = FastAPI(root_path="/api/v1")
    app.include_router(controller_container.cahsier_controller)
    app.include_router(controller_container.member_controller)
    app.include_router(controller_container.product_controller)
    app.include_router(controller_container.report_controller)
    app.include_router(controller_container.user_controller)
    include_documentation(app)

    return app
