import uuid

from pydantic import BaseModel, Field


class BGGearItem(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    i_name: str = Field(...)
    effect: str = Field(...)
    source: str = Field(...)
    location: str = Field(...)

    class ConfigDict:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "i_name": "Everburn Blade",
                "effect": "Deal additional 1d4 Fire damage with this weapon",
                "source": "Commander Zhalk at the helm of the ship",
                "location": "Nautiloid X:53 Y:390"
            }
        }
