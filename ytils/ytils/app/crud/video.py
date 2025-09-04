from pydantic import BaseModel, Field
from app.logger import logger
from typing import List
from app.db import Database, get_database
from app.minio import save_to_minio, get_from_minio, list_all_objects
from app.settings import settings
from bson import ObjectId


db: Database
db = get_database("ytils", "videos")


class YoutubeVideo(BaseModel):
    id: ObjectId = Field(..., alias="_id")
    video_id: str  # this is youtube's assigned value, not the database id
    title: str = None
    artist: str = None
    album: str = None
    tags: List[str] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str
        }
    }

    def store_in_minio(self, file_path):
        with open(file_path, 'rb') as fobj:
            file_data = fobj.read()
            model_bucket = save_to_minio(bucket_name=settings.minio_video_bucket,
                                         object_name=str(self.id),
                                         file_data=file_data,
                                         content_type="application/octet-stream")

            return model_bucket

    def get_from_minio(self):
        return get_from_minio(settings.minio_video_bucket, object_name=str(self.id))

    async def update(self, **kwargs):
        logger.info(kwargs)
        update_fields = {k: v for k, v in kwargs.items() if hasattr(self, k)}

        if not update_fields:
            return  # Nothing to update

        # Update the document in MongoDB
        result = await db.collection.update_one({"_id": self.id}, {"$set": update_fields})
        logger.debug(f"Update result {result}")


async def create(**video_dict) -> YoutubeVideo:
    logger.info(f"{video_dict=}")
    result = await db.collection.insert_one(video_dict)
    logger.info(f"inserted key: {result.inserted_id}")
    video_dict["_id"] = result.inserted_id
    video = YoutubeVideo(**video_dict)
    return video


async def find_one(**kwargs) -> YoutubeVideo:
    search_filter = dict(kwargs)

    docs = await db.collection.find(filter=search_filter).to_list()
    if not docs:
        return None

    return YoutubeVideo(**docs[0])


async def find(**kwargs) -> List[YoutubeVideo]:
    search_filter = dict(kwargs)

    docs = await db.collection.find(filter=search_filter).to_list()
    if not docs:
        return None

    return [YoutubeVideo(**doc) for doc in docs]


async def get(id: str) -> YoutubeVideo:
    search_filter = {"_id": ObjectId(id)}
    doc = await db.collection.find_one(filter=search_filter)

    if not doc:
        return None

    api_key = YoutubeVideo(**doc)
    return api_key


async def purge_db_objects():
    await db.collection.delete_many({})


def list_minio_objects():
    objects = list_all_objects(settings.minio_video_bucket)
    return objects
