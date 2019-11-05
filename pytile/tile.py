"""Define endpoints for interacting with Tiles."""
from typing import Awaitable, Callable, List, Optional


class Tile:  # pylint: disable=too-few-public-methods
    """Define "Tile" endpoints."""

    def __init__(
        self,
        request: Callable[..., Awaitable[dict]],
        *,
        user_uuid: Optional[str] = None,
    ) -> None:
        """Initialize."""
        self._request: Callable[..., Awaitable[dict]] = request
        self._user_uuid: Optional[str] = user_uuid

    async def all(self, whitelist: list = None, show_inactive: bool = False) -> list:
        """Get all Tiles for a user's account."""
        list_data: dict = await self._request(
            "get", f"users/{self._user_uuid}/user_tiles"
        )
        tile_uuid_list: List[str] = [
            tile["tile_uuid"]
            for tile in list_data["result"]
            if not whitelist or tile["tileType"] in whitelist
        ]

        tile_data: dict = await self._request(
            "get", "tiles", params=[("tile_uuids", uuid) for uuid in tile_uuid_list]
        )
        return [
            tile
            for tile in tile_data["result"].values()
            if show_inactive or tile["visible"] is True
        ]
