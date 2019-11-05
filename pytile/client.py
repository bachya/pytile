"""Define a client to interact with Pollen.com."""
from typing import Optional
from uuid import uuid4

from aiohttp import ClientSession, client_exceptions

from .errors import RequestError, SessionExpiredError
from .tile import Tile
from .util import current_epoch_time

API_URL_SCAFFOLD: str = "https://production.tile-api.com/api/v1"
DEFAULT_APP_ID: str = "ios-tile-production"
DEFAULT_APP_VERSION: str = "2.55.1.3707"
DEFAULT_LOCALE: str = "en-US"


class Client:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """Define the client."""

    def __init__(
        self,
        email: str,
        password: str,
        websession: ClientSession,
        *,
        client_uuid: Optional[str] = None,
        locale: str = DEFAULT_LOCALE,
    ) -> None:
        """Initialize."""
        self._client_established: bool = False
        self._email: str = email
        self._locale: str = locale
        self._password: str = password
        self._session_expiry: Optional[int] = None
        self._websession: ClientSession = websession
        self.tiles: Optional[Tile] = None
        self.user_uuid: Optional[str] = None

        self.client_uuid: str
        if not client_uuid:
            self.client_uuid = str(uuid4())
        else:
            self.client_uuid = client_uuid

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> dict:
        """Make a request against AirVisual."""
        if self._session_expiry and self._session_expiry <= current_epoch_time():
            raise SessionExpiredError("Session has expired; make a new one!")

        if not headers:
            headers = {}
        headers.update(
            {
                "Tile_app_id": DEFAULT_APP_ID,
                "Tile_app_version": DEFAULT_APP_VERSION,
                "Tile_client_uuid": self.client_uuid,
            }
        )

        async with self._websession.request(
            method,
            f"{API_URL_SCAFFOLD}/{endpoint}",
            headers=headers,
            params=params,
            data=data,
        ) as resp:
            try:
                resp.raise_for_status()
                return await resp.json(content_type=None)
            except client_exceptions.ClientError as err:
                raise RequestError(
                    f"Error requesting data from {endpoint}: {err}"
                ) from None

    async def async_init(self) -> None:
        """Create a Tile session."""
        if not self._client_established:
            await self._request(
                "put",
                f"clients/{self.client_uuid}",
                data={
                    "app_id": DEFAULT_APP_ID,
                    "app_version": DEFAULT_APP_VERSION,
                    "locale": self._locale,
                },
            )
            self._client_established = True

        resp: dict = await self._request(
            "post",
            f"clients/{self.client_uuid}/sessions",
            data={"email": self._email, "password": self._password},
        )

        if not self.user_uuid:
            self.user_uuid = resp["result"]["user"]["user_uuid"]
        self._session_expiry = resp["result"]["session_expiration_timestamp"]

        self.tiles = Tile(self._request, user_uuid=self.user_uuid)


async def async_login(
    email: str,
    password: str,
    websession: ClientSession,
    *,
    client_uuid: Optional[str] = None,
    locale: str = DEFAULT_LOCALE,
) -> Client:
    """Return an authenticated client."""
    client = Client(email, password, websession, client_uuid=client_uuid, locale=locale)
    await client.async_init()
    return client
