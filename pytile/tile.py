"""Define a Tile object."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any, cast

from .const import LOGGER


class Tile:
    """Define a Tile."""

    def __init__(
        self,
        async_request: Callable[..., Awaitable[dict[str, Any]]],
        tile_data: dict[str, Any],
    ) -> None:
        """Initialize.

        Args:
            async_request: The request method from the Client object.
            tile_data: A dictionary of Tile data.
        """
        self._async_request = async_request
        self._tile_data = tile_data

        self._last_timestamp: datetime | None = None
        self._lost_timestamp: datetime | None = None
        self._save_timestamps(tile_data)

    def __str__(self) -> str:
        """Return the string representation of the Tile.

        Returns:
            A string representation.
        """
        return f"<Tile uuid={self.uuid} name={self.name}>"

    @property
    def accuracy(self) -> float | None:
        """Return the accuracy of the last measurement.

        Returns:
            The accuracy (if it exists).
        """
        if (last_state := self._tile_data["result"].get("last_tile_state")) is None:
            return None
        return cast(float, last_state["h_accuracy"])

    @property
    def altitude(self) -> float | None:
        """Return the last detected altitude.

        Returns:
            The altitude (if it exists).
        """
        if (last_state := self._tile_data["result"].get("last_tile_state")) is None:
            return None
        return cast(float, last_state["altitude"])

    @property
    def archetype(self) -> str:
        """Return the archetype.

        Returns:
            The archetype.
        """
        return cast(str, self._tile_data["result"]["archetype"])

    @property
    def dead(self) -> bool:
        """Return whether the Tile is dead.

        Returns:
            The dead status.
        """
        return cast(bool, self._tile_data["result"]["is_dead"])

    @property
    def firmware_version(self) -> str:
        """Return the firmware version.

        Returns:
            The firmware version.
        """
        return cast(str, self._tile_data["result"]["firmware_version"])

    @property
    def hardware_version(self) -> str:
        """Return the hardware version.

        Returns:
            The hardware version.
        """
        return cast(str, self._tile_data["result"]["hw_version"])

    @property
    def kind(self) -> str:
        """Return the type of Tile.

        Returns:
            The type.
        """
        return cast(str, self._tile_data["result"]["tile_type"])

    @property
    def last_timestamp(self) -> datetime | None:
        """Return the timestamp of the last location measurement.

        Returns:
            The timestamp (if it exists).
        """
        return self._last_timestamp

    @property
    def latitude(self) -> float | None:
        """Return the last detected latitude.

        Returns:
            The latitude (if it exists).
        """
        if (last_state := self._tile_data["result"].get("last_tile_state")) is None:
            return None
        return cast(float, last_state["latitude"])

    @property
    def longitude(self) -> float | None:
        """Return the last detected longitude.

        Returns:
            The longitude (if it exists).
        """
        if (last_state := self._tile_data["result"].get("last_tile_state")) is None:
            return None
        return cast(float, last_state["longitude"])

    @property
    def lost(self) -> bool:
        """Return whether the Tile is lost.

        Since the Tile API can sometimes fail to return last_tile_state data, if it's
        missing here, we return True (indicating the Tile *is* lost).

        Returns:
            The lost status.
        """
        if (last_state := self._tile_data["result"].get("last_tile_state")) is None:
            return True
        return cast(bool, last_state["is_lost"])

    @property
    def lost_timestamp(self) -> datetime | None:
        """Return the timestamp when the Tile was last in a "lost" state.

        Returns:
            The timestamp (if it exists).
        """
        return self._lost_timestamp

    @property
    def name(self) -> str:
        """Return the name.

        Returns:
            The name.
        """
        return cast(str, self._tile_data["result"]["name"])

    @property
    def ring_state(self) -> str | None:
        """Return the ring state.

        Returns:
            The ring state (if it exists).
        """
        if (last_state := self._tile_data["result"].get("last_tile_state")) is None:
            return None
        return cast(str, last_state["ring_state"])

    @property
    def uuid(self) -> str:
        """Return the UUID.

        Returns:
            The UUID.
        """
        return cast(str, self._tile_data["result"]["tile_uuid"])

    @property
    def visible(self) -> bool:
        """Return whether the Tile is visible.

        Returns:
            The visibility.
        """
        return cast(bool, self._tile_data["result"]["visible"])

    @property
    def voip_state(self) -> str | None:
        """Return the VoIP state.

        Returns:
            The VoIP state (if it exists).
        """
        if (last_state := self._tile_data["result"].get("last_tile_state")) is None:
            return None
        return cast(str, last_state["voip_state"])

    def _save_timestamps(self, tile_data: dict[str, Any]) -> None:
        """Save UTC timestamps from a Tile data set.

        Args:
            tile_data: A dictionary of Tile data.
        """
        if (last_state := tile_data["result"].get("last_tile_state")) is None:
            LOGGER.warning("Missing last_tile_state; can't report location info")
            self._last_timestamp = None
            self._lost_timestamp = None
            return

        self._last_timestamp = datetime.utcfromtimestamp(last_state["timestamp"] / 1000)
        self._lost_timestamp = datetime.utcfromtimestamp(
            last_state["lost_timestamp"] / 1000
        )

    def as_dict(self) -> dict[str, Any]:
        """Return dictionary version of this Tile.

        Returns:
            A dictionary representation of the Tile.
        """
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
