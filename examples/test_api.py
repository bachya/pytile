"""Run an example script to quickly test."""
import asyncio
import logging

from aiohttp import ClientSession

from pytile import async_login
from pytile.errors import TileError

_LOGGER = logging.getLogger(__name__)

TILE_EMAIL = "<EMAIL>"
TILE_PASSWORD = "<PASSWORD>"  # noqa: S105


async def main() -> None:
    """Run."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            api = await async_login(TILE_EMAIL, TILE_PASSWORD, session)

            tiles = await api.async_get_tiles()
            _LOGGER.info("Tile Count: %s", len(tiles))
            for tile in tiles.values():
                _LOGGER.info("UUID: %s", tile.uuid)
                _LOGGER.info("Name: %s", tile.name)
                _LOGGER.info("Type: %s", tile.kind)
                _LOGGER.info("Latitude: %s", tile.latitude)
                _LOGGER.info("Longitude: %s", tile.longitude)
                _LOGGER.info("Last Timestamp: %s", tile.last_timestamp)
        except TileError as err:
            _LOGGER.info(err)


asyncio.run(main())
