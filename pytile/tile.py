"""Define a Tile object."""
from datetime import datetime
from typing import Awaitable, Callable

TASK_DETAILS = "details"
TASK_MEASUREMENTS = "measurements"


class Tile:
    """Define a Tile."""

    def __init__(
        self, async_request: Callable[..., Awaitable], tile_data: dict
    ) -> None:
        """Initialize."""
        self._async_request = async_request
        self._last_timestamp: datetime = datetime.utcfromtimestamp(
            tile_data["last_tile_state"]["timestamp"] / 1000
        )
        self._lost_timestamp: datetime = datetime.utcfromtimestamp(
            tile_data["last_tile_state"]["lost_timestamp"] / 1000
        )
        self._tile_data = tile_data

    def __str__(self) -> str:
        """Return the string representation of the Tile."""
        return f"<Tile uuid={self.uuid} name={self.name}>"

    @property
    def accuracy(self) -> float:
        """Return the accuracy of the last measurement."""
        return self._tile_data["last_tile_state"]["h_accuracy"]

    @property
    def altitude(self) -> float:
        """Return the last detected altitude."""
        return self._tile_data["last_tile_state"]["altitude"]

    @property
    def archetype(self) -> str:
        """Return the archetype."""
        return self._tile_data["archetype"]

    @property
    def dead(self) -> bool:
        """Return whether the Tile is dead."""
        return self._tile_data["is_dead"]

    @property
    def firmware_version(self) -> str:
        """Return the firmware version."""
        return self._tile_data["firmware_version"]

    @property
    def hardware_version(self) -> str:
        """Return the hardware version."""
        return self._tile_data["hw_version"]

    @property
    def kind(self) -> str:
        """Return the type of Tile."""
        return self._tile_data["tile_type"]

    @property
    def last_timestamp(self) -> datetime:
        """Return the timestamp of the last location measurement."""
        return self._last_timestamp

    @property
    def latitude(self) -> float:
        """Return the last detected latitude."""
        return self._tile_data["last_tile_state"]["latitude"]

    @property
    def longitude(self) -> float:
        """Return the last detected longitude."""
        return self._tile_data["last_tile_state"]["longitude"]

    @property
    def lost(self) -> bool:
        """Return whether the Tile is lost."""
        return self._tile_data["last_tile_state"]["is_lost"]

    @property
    def lost_timestamp(self) -> datetime:
        """Return the timestamp when the Tile was last in a "lost" state."""
        return self._lost_timestamp

    @property
    def name(self) -> str:
        """Return the name."""
        return self._tile_data["name"]

    @property
    def uuid(self) -> str:
        """Return the UUID."""
        return self._tile_data["tile_uuid"]

    @property
    def visible(self) -> bool:
        """Return whether the Tile is visible."""
        return self._tile_data["visible"]

    def _async_save_new_data(self, data: dict) -> None:
        """Save new Tile data in this object."""
        self._last_timestamp = datetime.utcfromtimestamp(
            data["result"]["last_tile_state"]["timestamp"] / 1000
        )
        self._lost_timestamp = datetime.utcfromtimestamp(
            data["result"]["last_tile_state"]["lost_timestamp"] / 1000
        )
        self._tile_data = data["result"]

    async def async_update(self) -> None:
        """Get the latest measurements from the Tile."""
        data = await self._async_request("get", f"tiles/{self.uuid}")
        self._async_save_new_data(data)
