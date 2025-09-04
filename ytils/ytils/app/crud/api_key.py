from pydantic import BaseModel, Field
from app.logger import logger
from typing import List
from app.db import Database, get_database
from bson import ObjectId


db: Database
db = get_database("test", "api_keys")


class YoutubeAPIKey(BaseModel):
    id: ObjectId = Field(..., alias="_id")
    key: str

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str
        }
    }


async def create(**api_key_dict) -> YoutubeAPIKey:
    logger.info(f"{api_key_dict=}")
    result = await db.collection.insert_one(api_key_dict)
    logger.info(f"inserted key: {result.inserted_id}")
    api_key_dict["_id"] = result.inserted_id
    api_key = YoutubeAPIKey(**api_key_dict)
    return api_key


async def find(**kwargs) -> List[YoutubeAPIKey]:
    search_filter = dict(kwargs)

    docs = await db.collection.find(filter=search_filter).to_list()
    if not docs:
        return None

    return [YoutubeAPIKey(**doc) for doc in docs]


async def get(id: str) -> YoutubeAPIKey:
    search_filter = {"_id": ObjectId(id)}
    doc = await db.collection.find_one(filter=search_filter)

    if not doc:
        return None

    api_key = YoutubeAPIKey(**doc)
    return api_key
