from fastapi import FastAPI
from adapters.db.mongodb.repositories.member import MemberRepository
from adapters.db.mongodb.transaction_provider import MongoDBTransactionProvider

from adapters.http.controllers.example import ExampleController, ExampleService

from pymongo import MongoClient

from core.services.member import MemberService
from security.bcrypt.hasher import BCryptPasswordHasher

app = FastAPI()

mongo_client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")

db = mongo_client.Test
test_collection = db.test
baru_collection = db.baru
member_collection = db.member

# member_repository = MemberRepository(member_collection)
# hasher = BCryptPasswordHasher()
# transaction_provider = MongoDBTransactionProvider(mongo_client)
# member_service = MemberService(member_repository, hasher)
# member_service.register('haziq10102@email.com', '123456', 'haziq')


@app.get("/")
def health():
    return {"Hello": "World"}


example_controller = ExampleController(ExampleService(10))

app.include_router(example_controller)
