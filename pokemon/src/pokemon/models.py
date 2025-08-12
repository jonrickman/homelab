import uuid
from typing import List

import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from pokemon.config import MONGODB_URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
pokemon_collection = client.pokemon["pokemon"]


class PokemonStats(BaseModel):
    hp: int = Field(...)
    attack: int = Field(...)
    defense: int = Field(...)
    special_attack: int = Field(...)
    special_defense: int = Field(...)
    speed: int = Field(...)


class Encounter(BaseModel):
    condition_values: str = Field(...)
    chance: int = Field(...)
    min_level: int = Field(...)
    max_level: int = Field(...)
    method: str = Field(...)

    def pretty(self):
        conditional = f"{self.chance}% {self.method} {self.condition_values}"
        level_range = f"{self.min_level}-{self.max_level}" if self.min_level != self.max_level else self.min_level
        return f"{conditional} -- {level_range}"


class Location(BaseModel):
    name: str = Field(...)
    version: str = Field(...)
    encounters: List[Encounter] = Field(...)

    def pretty(self):
        return [f"{self.name}-{self.version}--{e.pretty()}" for e in self.encounters]


class Pokemon(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    pokedex_number: int = Field(...)
    abilities: List[str] = Field(...)
    pokemon_name: str = Field(...)

    stats: PokemonStats = Field(...)

    locations: List[Location] = Field(...)
    moveset: List[str] = Field(...)

    class ConfigDict:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {

            }
        }

    async def insert(self):
        item = jsonable_encoder(self)
        new_item = await pokemon_collection.insert_one(item)
        created_item = await pokemon_collection.find_one({"_id": new_item.inserted_id})
        return created_item

    def pretty_locations(self):
        locations = [location.pretty() for location in self.locations]
        return locations
