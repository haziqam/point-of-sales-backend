from pymongo import MongoClient


class DbContainer:
    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self.db = client.PosDB
