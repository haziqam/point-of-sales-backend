import os
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from containers.repository import RepositoryContainer
from infrastructure.containers.db import DbContainer

# from infrastructure.adapters.db.mongodb.repositories

load_dotenv()


# def start_app() -> FastAPI:
#     db_container = DbContainer(
#         MongoClient(
#             os.getenv("CONN_STRING", "mongodb://localhost:27017/?replicaSet=rs0")
#         )
#     )

#     repository_container = RepositoryContainer(BillRepository)
