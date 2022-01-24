"""Define a Tile object."""
from datetime import datetime
import logging
from typing import Any, Awaitable, Callable, Dict, Optional

_LOGGER = logging.getLogger(__name__)


class Tile:
    """Define a Tile."""

    def __init__(
        self, async_request: Callable[..., Awaitable], tile_data: dict
    ) -> None:
        """Initialize."""
        self._async_request = async_request
        self._tile_data = tile_data

        self._last_timestamp: Optional[datetime] = None
        self._lost_timestamp: Optional[datetime] = None
        self._save_timestamps(tile_data)

    def __str__(self) -> str:
        """Return the string representation of the Tile."""
        return f"<Tile uuid={self.uuid} name={self.name}>"

    @property
    def accuracy(self) -> Optional[float]:
        """Return the accuracy of the last measurement."""
        if not self._tile_data["result"].get("last_tile_state"):
            return None
        return self._tile_data["result"]["last_tile_state"]["h_accuracy"]

    @property
    def altitude(self) -> Optional[float]:
        """Return the last detected altitude."""
        if not self._tile_data["result"].get("last_tile_state"):
            return None
        return self._tile_data["result"]["last_tile_state"]["altitude"]

    @property
    def archetype(self) -> str:
        """Return the archetype."""
        return self._tile_data["result"]["archetype"]

    @property
    def dead(self) -> bool:
        """Return whether the Tile is dead."""
        return self._tile_data["result"]["is_dead"]

    @property
    def firmware_version(self) -> str:
        """Return the firmware version."""
        return self._tile_data["result"]["firmware_version"]

    @property
    def hardware_version(self) -> str:
        """Return the hardware version."""
        return self._tile_data["result"]["hw_version"]

    @property
    def kind(self) -> str:
        """Return the type of Tile."""
        return self._tile_data["result"]["tile_type"]

    @property
    def last_timestamp(self) -> Optional[datetime]:
        """Return the timestamp of the last location measurement."""
        return self._last_timestamp

    @property
    def latitude(self) -> Optional[float]:
        """Return the last detected latitude."""
        if not self._tile_data["result"].get("last_tile_state"):
            return None
        return self._tile_data["result"]["last_tile_state"]["latitude"]

    @property
    def longitude(self) -> Optional[float]:
        """Return the last detected longitude."""
        if not self._tile_data["result"].get("last_tile_state"):
            return None
        return self._tile_data["result"]["last_tile_state"]["longitude"]

    @property
    def lost(self) -> bool:
        """
        Return whether the Tile is lost.

        Since the Tile API can sometimes fail to return last_tile_state data, if it's
        missing here, we return True (indicating the Tile *is* lost).
        """
        if not self._tile_data["result"].get("last_tile_state"):
            return True
        return self._tile_data["result"]["last_tile_state"]["is_lost"]

    @property
    def lost_timestamp(self) -> Optional[datetime]:
        """Return the timestamp when the Tile was last in a "lost" state."""
        return self._lost_timestamp

    @property
    def name(self) -> str:
        """Return the name."""
        return self._tile_data["result"]["name"]

    @property
    def ring_state(self) -> Optional[str]:
        """Return the ring state."""
        if not self._tile_data["result"].get("last_tile_state"):
            return None
        return self._tile_data["result"]["last_tile_state"]["ring_state"]

    @property
    def uuid(self) -> str:
        """Return the UUID."""
        return self._tile_data["result"]["tile_uuid"]

    @property
    def visible(self) -> bool:
        """Return whether the Tile is visible."""
        return self._tile_data["result"]["visible"]

    @property
    def voip_state(self) -> Optional[str]:
        """Return the VoIP state."""
        if not self._tile_data["result"].get("last_tile_state"):
            return None
        return self._tile_data["result"]["last_tile_state"]["voip_state"]

    def _save_timestamps(self, tile_data: dict) -> None:
        """Save UTC timestamps from a Tile data set."""
        if not tile_data["result"].get("last_tile_state"):
            _LOGGER.warning("Missing last_tile_state; can't report location info")
            self._last_timestamp = None
            self._lost_timestamp = None
            return

        self._last_timestamp = datetime.utcfromtimestamp(
            tile_data["result"]["last_tile_state"]["timestamp"] / 1000
        )
        self._lost_timestamp = datetime.utcfromtimestamp(
            tile_data["result"]["last_tile_state"]["lost_timestamp"] / 1000
        )

    def as_dict(self) -> Dict[str, Any]:
        """Return dictionary version of this Tile."""
        return {
            "accuracy": self.accuracy,
            "altitude": self.altitude,
            "archetype": self.archetype,
            "dead": self.dead,
            "firmware_version": self.firmware_version,
            "hardware_version": self.hardware_version,
            "kind": self.kind,
            "last_timestamp": self.last_timestamp,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "lost": self.lost,
            "lost_timestamp": self.lost_timestamp,
            "name": self.name,
            "ring_state": self.ring_state,
            "uuid": self.uuid,
            "visible": self.visible,
            "voip_state": self.voip_state,
        }

    async def async_update(self) -> None:
        """Get the latest measurements from the Tile."""
        data = await self._async_request("get", f"tiles/{self.uuid}")
        self._save_timestamps(data)
        self._tile_data = data
