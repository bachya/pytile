"""Define endpoints for interacting with Tiles."""
from typing import Awaitable, Callable


class Tile(object):  # pylint: disable=too-few-public-methods
    """Define "Tile" endpoints."""

    def __init__(
            self, request: Callable[..., Awaitable[dict]],
            user_uuid: str) -> None:
        """Initialize."""
        self._request = request
        self._user_uuid = user_uuid

    async def all(
            self, whitelist: list = None, show_inactive: bool = False) -> list:
        """Get all Tiles for a user's account."""
        list_data = await self._request(
            'get', 'users/{0}/user_tiles'.format(self._user_uuid))
        tile_uuid_list = [
            tile['tile_uuid'] for tile in list_data['result']
            if not whitelist or tile['tileType'] in whitelist
        ]

        tile_data = await self._request(
            'get',
            'tiles',
            params=[('tile_uuids', uuid) for uuid in tile_uuid_list])
        return [
            tile for tile in tile_data['result'].values() if show_inactive
            or tile['tileState']['connection_state'] == 'READY'
        ]
