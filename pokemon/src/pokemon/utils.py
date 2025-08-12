import asyncio
import json

import motor.motor_asyncio
import requests

from pokemon.config import MONGODB_URL
from pokemon.models import Encounter, Location, Pokemon, PokemonStats

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
pokemon_collection = client.pokemon["pokemon"]


async def drop_pokemon_table():
    await pokemon_collection.drop()


async def list_pokemon():
    poekmon = await pokemon_collection.find().to_list(1025)
    return poekmon


async def find_pokemon(query: str):
    pokemon = await pokemon_collection.find({'pokemon_name': {'$regex': query, '$options': 'i'}}).to_list(10)

    return [Pokemon(**p) for p in pokemon]


def download_manifests(pokedex_number: int) -> None:
    # https://pokeapi.co/api/v2/pokemon/1/
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokedex_number}"
    response = requests.get(api_url)
    with open(f"./manifests/{pokedex_number}.json", "w") as fobj:
        json.dump(response.json(), fobj)

    # https://pokeapi.co/api/v2/pokemon/1/encounters
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokedex_number}/encounters"
    response = requests.get(api_url)
    with open(f"./manifests/{pokedex_number}-encounters.json", "w") as fobj:
        json.dump(response.json(), fobj)


async def parse_pokemon(pokedex_number: int) -> Pokemon:

    #  parse the manifest for the pokedex entry
    with open(f"./manifests/{pokedex_number}.json", "r") as fobj:
        data = json.load(fobj)

    pokemon_name = data["name"]

    abilities = [d["ability"]["name"] for d in data["abilities"]]

    stat_dict = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}

    stats = PokemonStats(hp=stat_dict["hp"],
                         attack=stat_dict["attack"],
                         defense=stat_dict["defense"],
                         special_attack=stat_dict["special-attack"],
                         special_defense=stat_dict["special-defense"],
                         speed=stat_dict["speed"])

    # parse the encounter entry
    with open(f"./manifests/{pokedex_number}-encounters.json", "r") as fobj:
        items = json.load(fobj)

    locations = []

    # iterate the items and build details
    for item in items:
        location_name = item["location_area"]["name"]
        versions = item["version_details"]

        # each version has its own
        for version in versions:
            version_name = version["version"]["name"]
            encounter_details = version["encounter_details"]

            encounters = []

            # there can be multiple encounter values because of conditionals/methods
            for encounter in encounter_details:
                chance = encounter["chance"]
                condition_values = "".join([e["name"] for e in encounter["condition_values"]])
                max_level = encounter["max_level"]
                min_level = encounter["min_level"]
                method = encounter["method"]["name"]

                # append the encounter
                encounters.append(Encounter(condition_values=condition_values,
                                            chance=chance,
                                            max_level=max_level,
                                            min_level=min_level,
                                            method=method))

            # append the location
            locations.append(Location(name=location_name,
                                      version=version_name,
                                      encounters=encounters))

        pokemon = Pokemon(pokedex_number=pokedex_number,
                          abilities=abilities,
                          pokemon_name=pokemon_name,
                          locations=locations,
                          stats=stats,
                          moveset=[])

        # add it to the database and return
        # TODO: exception handle this
        await pokemon.insert()
        return pokemon


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(drop_pokemon_table())

    for i in range(1, 1026):
        #    download_manifests(i)
        loop.run_until_complete(parse_pokemon(i))
