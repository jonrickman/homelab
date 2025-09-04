from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection

from app.logger import logger
from app.settings import settings


class Database:
    mongo_url: str
    mongo_client: AsyncIOMotorClient
    collection: Collection
    default_record_count: int

    def __init__(self, database_name: str = None, collection_name: str = None) -> None:
        logger.debug("Connecting to Mongo!")
        self.mongo_url = settings.mongo_url
        self.mongo_client = AsyncIOMotorClient(self.mongo_url)

        logger.info(f"Mongo URL {self.mongo_url}")
        # set the database & collection specifics
        if database_name:
            self.mongo_db = self.mongo_client[database_name]
        else:
            self.mongo_db = self.mongo_client[settings.default_db]

        if collection_name:
            self.collection = self.mongo_db[collection_name]
        else:
            self.collection = self.mongo_db[settings.default_collection]

        logger.info("Connected to Mongo!")


def get_database(database_name: str = None, collection_name: str = None) -> Database:
    """
    Create a Database and return it -- done as syntactial sugar currently though perhaps future work
    may require this.

    Returns:
        A new Database object
    """
    return Database(database_name, collection_name)
