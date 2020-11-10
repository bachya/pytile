"""Define a Tile object."""
from datetime import datetime
import logging
from typing import Awaitable, Callable, Optional

_LOGGER = logging.getLogger(__name__)

TASK_DETAILS = "details"
TASK_MEASUREMENTS = "measurements"


class Tile:
    """Define a Tile."""

    def __init__(
        self, async_request: Callable[..., Awaitable], tile_data: dict
    ) -> None:
        """Initialize."""
        self._async_request = async_request
        self._tile_data = tile_data

        try:
            self._last_timestamp: Optional[datetime] = datetime.utcfromtimestamp(
                tile_data["last_tile_state"]["timestamp"] / 1000
            )
            self._lost_timestamp: Optional[datetime] = datetime.utcfromtimestamp(
                tile_data["last_tile_state"]["lost_timestamp"] / 1000
            )
        except TypeError:
            _LOGGER.warning(
                "Response missing last_tile_state; can't report location info"
            )
            self._last_timestamp = None
            self._lost_timestamp = None

    def __str__(self) -> str:
        """Return the string representation of the Tile."""
        return f"<Tile uuid={self.uuid} name={self.name}>"

    @property
    def accuracy(self) -> Optional[float]:
        """Return the accuracy of the last measurement."""
        try:
            return self._tile_data["last_tile_state"]["h_accuracy"]
        except TypeError:
            return None

    @property
    def altitude(self) -> Optional[float]:
        """Return the last detected altitude."""
        try:
            return self._tile_data["last_tile_state"]["altitude"]
        except TypeError:
            return None

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
    def last_timestamp(self) -> Optional[datetime]:
        """Return the timestamp of the last location measurement."""
        return self._last_timestamp

    @property
    def latitude(self) -> Optional[float]:
        """Return the last detected latitude."""
        try:
            return self._tile_data["last_tile_state"]["latitude"]
        except TypeError:
            return None

    @property
    def longitude(self) -> Optional[float]:
        """Return the last detected longitude."""
        try:
            return self._tile_data["last_tile_state"]["longitude"]
        except TypeError:
            return None

    @property
    def lost(self) -> bool:
        """Return whether the Tile is lost."""
        try:
            return self._tile_data["last_tile_state"]["is_lost"]
        except TypeError:
            return False

    @property
    def lost_timestamp(self) -> Optional[datetime]:
        """Return the timestamp when the Tile was last in a "lost" state."""
        return self._lost_timestamp

    @property
    def name(self) -> str:
        """Return the name."""
        return self._tile_data["name"]

    @property
    def ring_state(self) -> str:
        """Return the ring state."""
        return self._tile_data["last_tile_state"]["ring_state"]

    @property
    def uuid(self) -> str:
        """Return the UUID."""
        return self._tile_data["tile_uuid"]

    @property
    def visible(self) -> bool:
        """Return whether the Tile is visible."""
        return self._tile_data["visible"]

    @property
    def voip_state(self) -> str:
        """Return the VoIP state."""
        return self._tile_data["last_tile_state"]["voip_state"]

    def _async_save_new_data(self, data: dict) -> None:
        """Save new Tile data in this object."""
        try:
            self._last_timestamp = datetime.utcfromtimestamp(
                data["result"]["last_tile_state"]["timestamp"] / 1000
            )
            self._lost_timestamp = datetime.utcfromtimestamp(
                data["result"]["last_tile_state"]["lost_timestamp"] / 1000
            )
        except TypeError:
            _LOGGER.warning(
                "Response missing last_tile_state; can't report location info"
            )
            self._last_timestamp = None
            self._lost_timestamp = None

        self._tile_data = data["result"]

    async def async_update(self) -> None:
        """Get the latest measurements from the Tile."""
        data = await self._async_request("get", f"tiles/{self.uuid}")
        self._async_save_new_data(data)
