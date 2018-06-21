"""Run an example script to quickly test."""
import asyncio

from aiohttp import ClientSession

from pytile import Client
from pytile.errors import TileError


async def tiles(client: Client) -> None:
    """Output allergen-related information."""
    print('ALL TILES')
    print(await client.tiles.all())


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        await run(websession)


async def run(websession):
    """Run."""
    try:
        # Create a client:
        client = Client(
            'bachya1208@gmail.com',
            'BaqPBzT)8uXQ@UPcqyjwDHuCu',
            websession,
            client_uuid='6a56daa3-1b70-4643-a509-62614d6ebc7b')
        await client.async_init()

        # Work with Tile data:
        await tiles(client)
    except TileError as err:
        print(err)


asyncio.get_event_loop().run_until_complete(main())
