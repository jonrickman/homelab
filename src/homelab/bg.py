import motor.motor_asyncio
import requests
from bs4 import BeautifulSoup
from fastapi.encoders import jsonable_encoder

from homelab.config import MONGODB_URL
from homelab.models import BGGearItem

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
collection = client.test["gear"]


async def drop_bg_items_table():
    await collection.drop()


async def list_bg_items():
    bg_items = await collection.find().to_list(1000)
    return bg_items


async def find_bg_item(query: str):
    items = await collection.find({'i_name': {'$regex': query, '$options': 'i'}}).to_list(1000)
    if items:
        return items
    items = await collection.find({'effect': {'$regex': query, '$options': 'i'}}).to_list(1000)
    return items


async def create_bg_gear_item(bg_item: BGGearItem):
    item = jsonable_encoder(bg_item)
    new_item = await collection.insert_one(item)
    created_item = await collection.find_one({"_id": new_item.inserted_id})
    return created_item


async def get_gear_locator_items():
    act_1_url = "https://bg3.wiki/wiki/Guide:Gear_locator"
    act_2_url = "https://bg3.wiki/wiki/Guide:Gear_locator_(Act_Two)"
    act_3_url = "https://bg3.wiki/wiki/Guide:Gear_locator_(Act_Three)"

    await parse(act_1_url)
    await parse(act_2_url)
    await parse(act_3_url)


async def parse(url: str) -> None:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all("table", class_="wikitable")
    for table in tables:
        soup = BeautifulSoup(str(table), 'html.parser')

        # default values set for scoping
        source = ""
        location = ""

        for tr in soup.find_all("tr"):
            i_name = [cell.text.strip() for cell in tr.find_all('th')][0]
            if i_name == "Item name":
                continue
            tds = [cell.text.strip() for cell in tr.find_all('td')]

            # Sometimes there is no data in a tr
            if not tds:
                continue

            tag_count = len(tds)

            # if there are more than 3 items in the table then it is malformed
            if tag_count > 3:
                # TODO: log these... maybe something useful
                continue

            # if only one matching tag then it should be a vendor or shared source&location
            if tag_count == 1:
                # already read the source & location so assume the previous -- note that this could be wrong
                if source and location:
                    effect = tds[0]
                    bg_item = BGGearItem(i_name=i_name, effect=effect, source=source, location=location)
                    await create_bg_gear_item(bg_item)
                    continue
                continue  # this edge case is if item is first in the table

            # sometimes there is no location
            if tag_count == 2:
                effect, source = tds
                location = ""  # don't want to assume location from previous entry
                bg_item = BGGearItem(i_name=i_name, effect=effect, source=source, location=location)
                await create_bg_gear_item(bg_item)
                continue

            effect, source, location = tds
            bg_item = BGGearItem(i_name=i_name, effect=effect, source=source, location=location)
            await create_bg_gear_item(bg_item)
