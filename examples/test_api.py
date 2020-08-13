"""Run an example script to quickly test."""
import asyncio

from aiohttp import ClientSession

from pytile import async_login
from pytile.errors import TileError

TILE_EMAIL = "bachya1208@gmail.com"
TILE_PASSWORD = "}oeoGpGpVFh8VTFhKDzi"


async def main():
    """Run."""
    async with ClientSession() as session:
        try:
            api = await async_login(TILE_EMAIL, TILE_PASSWORD, session)

            tiles = await api.async_get_tiles()
            print(f"Tile Count: {len(tiles)}")
            print()

            for tile in tiles.values():
                print(f"UUID: {tile.uuid}")
                print(f"Name: {tile.name}")
                print(f"Type: {tile.kind}")
                print(f"Latitude: {tile.latitude}")
                print(f"Longitude: {tile.longitude}")
                print(f"Last Timestamp: {tile.last_timestamp}")
                print()
        except TileError as err:
            print(err)


asyncio.run(main())
