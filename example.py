"""Run an example script to quickly test."""
import asyncio

from aiohttp import ClientSession

from pytile import async_login
from pytile.errors import TileError


async def main():
    """Run."""
    async with ClientSession() as websession:
        try:
            # Create a client:
            client = await async_login("<EMAIL>", "<PASSWORD>", websession)

            print("Showing active Tiles:")
            print(await client.tiles.all())

            print("Showing all Tiles:")
            print(await client.tiles.all(show_inactive=True))
        except TileError as err:
            print(err)


asyncio.get_event_loop().run_until_complete(main())
