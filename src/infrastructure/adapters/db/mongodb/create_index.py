from pymongo.database import Database


def create_index(db: Database) -> None:
    """
    Defines all indexes in the collections
    """
    db.member.create_index("email", unique=True)
    db.user.create_index("email", unique=True)
    db.product.create_index("name")
