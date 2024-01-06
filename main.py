from fastapi import FastAPI
from adapters.db.mongodb.repositories.cash import CashRepository
from adapters.db.mongodb.repositories.member import MemberRepository
from adapters.db.mongodb.repositories.product import ProductRepository
from adapters.db.mongodb.repositories.user import UserRepository
from adapters.db.mongodb.transaction_provider import MongoDBTransactionProvider
from adapters.rest.controllers.example import ExampleController, ExampleService
from core.models.user import User, Role

from pymongo import MongoClient
from core.models.member import VIPMember

from core.services.member import MemberService
from security.bcrypt.hasher import BCryptPasswordHasher

app = FastAPI()

mongo_client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")

db = mongo_client.Test
test_collection = db.test
baru_collection = db.baru
member_collection = db.member

member_repository = MemberRepository(member_collection)
# member = member_repository.find_member_by_id("659924b1feb454a35c5ed627")
# if member is not None:
#     print(member.dict())

user_repository = UserRepository(db.user)
# user_repository.create_user('Haziq', Role.MANAGER, 'haziq@email.com', '1234' )
# member = member_repository.create_member(
#     email="halodunia", hashed_PIN="1234567", name="namaku"
# )
# member.email = "validemail@example.com"
# member.public_data.name = "Beneran nama loh"
# vip_member = VIPMember.from_member(member, 0.5)
# member_repository.update_member(vip_member)

# hasher = BCryptPasswordHasher()
# transaction_provider = MongoDBTransactionProvider(mongo_client)
# member_service = MemberService(member_repository, hasher)
# member_service.register('haziq10102@email.com', '123456', 'haziq')


@app.get("/")
def health():
    return {"Hello": "World"}


example_controller = ExampleController(ExampleService(10))

app.include_router(example_controller)
