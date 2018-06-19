"""Define endpoints for interacting with Tiles."""


class Tile(object):  # pylint: disable=too-few-public-methods
    """Define "Tile" endpoints."""

    def __init__(self, request, user_uuid):
        """Initialize."""
        self._request = request
        self._user_uuid = user_uuid

    async def all(self, whitelist: list = None, show_inactive: bool = False):
        """Get all Tiles for a user's account."""
        list_data = await self._request(
            'get', 'users/{0}/user_tiles'.format(self._user_uuid))
        tile_uuid_list = [
            tile['tile_uuid'] for tile in list_data['result']
            if not whitelist or tile['tileType'] in whitelist
        ]

        tile_data = self._request(
            'get', 'tiles', json={'tile_uuids': tile_uuid_list})
        return [
            tile for tile in tile_data['result'].values() if show_inactive
            or tile['tileState']['connection_state'] == 'READY'
        ]
