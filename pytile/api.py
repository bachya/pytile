"""Define an object to work directly with the API."""
import asyncio
import logging
from time import time
from typing import Dict, Optional
from uuid import uuid4

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError

from .errors import RequestError
from .tile import Tile

_LOGGER = logging.getLogger(__name__)

API_URL_SCAFFOLD: str = "https://production.tile-api.com/api/v1"

DEFAULT_APP_ID: str = "ios-tile-production"
DEFAULT_APP_VERSION: str = "2.69.0.4123"
DEFAULT_LOCALE: str = "en-US"
DEFAULT_TIMEOUT: int = 10


class API:  # pylint: disable=too-many-instance-attributes
    """Define the API management object."""

    def __init__(
        self,
        email: str,
        password: str,
        session: ClientSession,
        *,
        client_uuid: Optional[str] = None,
        locale: str = DEFAULT_LOCALE,
    ) -> None:
        """Initialize."""
        self._client_established: bool = False
        self._email: str = email
        self._locale: str = locale
        self._password: str = password
        self._session: ClientSession = session
        self._session_expiry: Optional[int] = None
        self.client_uuid: str = str(uuid4()) if not client_uuid else client_uuid
        self.user_uuid: Optional[str] = None

    async def async_get_tiles(self) -> Dict[str, Tile]:
        """Get all active Tiles from the user's account."""
        states = await self.async_request("get", "tiles/tile_states")

        details_tasks = {
            tile_uuid: self.async_request("get", f"tiles/{tile_uuid}")
            for tile_uuid in [tile["tile_id"] for tile in states["result"]]
        }

        results = await asyncio.gather(*details_tasks.values())

        return {
            tile_uuid: Tile(self.async_request, tile_data["result"])
            for tile_uuid, tile_data, in zip(details_tasks, results)
        }

    async def async_init(self) -> None:
        """Create a Tile session."""
        # Invalidate the existing session expiry datetime (if it exists) so that the
        # next few requests don't fail:
        self._session_expiry = None

        if not self._client_established:
            await self.async_request(
                "put",
                f"clients/{self.client_uuid}",
                data={
                    "app_id": DEFAULT_APP_ID,
                    "app_version": DEFAULT_APP_VERSION,
                    "locale": self._locale,
                },
            )
            self._client_established = True

        resp = await self.async_request(
            "post",
            f"clients/{self.client_uuid}/sessions",
            data={"email": self._email, "password": self._password},
        )

        if not self.user_uuid:
            self.user_uuid = resp["result"]["user"]["user_uuid"]
        self._session_expiry = resp["result"]["session_expiration_timestamp"]

    async def async_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make a request against AirVisual."""
        if self._session_expiry and self._session_expiry <= int(time() * 1000):
            await self.async_init()

        kwargs.setdefault("headers", {})
        kwargs["headers"].update(
            {
                "Tile_app_id": DEFAULT_APP_ID,
                "Tile_app_version": DEFAULT_APP_VERSION,
                "Tile_client_uuid": self.client_uuid,
            }
        )

        async with self._session.request(
            method, f"{API_URL_SCAFFOLD}/{endpoint}", **kwargs
        ) as resp:
            try:
                resp.raise_for_status()
                data = await resp.json()
            except ClientError as err:
                raise RequestError(
                    f"Error requesting data from {endpoint}: {err}"
                ) from None

        _LOGGER.debug("Data received from /%s: %s", endpoint, data)

        return data


async def async_login(
    email: str,
    password: str,
    session: ClientSession,
    *,
    client_uuid: Optional[str] = None,
    locale: str = DEFAULT_LOCALE,
) -> API:
    """Return an authenticated client."""
    api = API(email, password, session, client_uuid=client_uuid, locale=locale)
    await api.async_init()
    return api
