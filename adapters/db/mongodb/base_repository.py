from pymongo.collection import Collection


class MongoDBRepository:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
