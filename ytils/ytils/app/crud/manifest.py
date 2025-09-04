import uuid
from pydantic import BaseModel, Field


class YoutubeVideoManifest(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    key: str = Field(...)

    class ConfigDict:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "key": "foobarbaz_id"
            }
        }
