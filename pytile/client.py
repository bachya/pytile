"""Define a client to interact with Pollen.com."""
from uuid import UUID, uuid4

from aiohttp import ClientSession, client_exceptions

from .errors import RequestError, SessionExpiredError
from .tile import Tile
from .util import current_epoch_time

API_URL_SCAFFOLD = 'https://production.tile-api.com/api/v1'
TILE_APP_ID = 'ios-tile-production'
TILE_APP_VERSION = '2.21.1'


class Client(object):  # pylint: disable=too-many-instance-attributes
    """Define the client."""

    def __init__(
            self,
            email: str,
            password: str,
            websession: ClientSession,
            *,
            client_uuid: UUID = None,
            locale: str = 'en-US') -> None:
        """Initialize."""
        self._client_confirmed = False
        self._email = email
        self._locale = locale
        self._password = password
        self._session_expiry = None
        self._user_uuid = None
        self._websession = websession
        self.tiles = None

        self._client_uuid = client_uuid
        if not self._client_uuid:
            self._client_uuid = str(uuid4())

    async def initialize(self):
        """Create a Tile session."""
        if not self._client_confirmed:
            await self.request(
                'put',
                'clients/{0}'.format(self._client_uuid),
                json={
                    'app_id': TILE_APP_ID,
                    'app_version': TILE_APP_VERSION,
                    'locale': self._locale,
                    'registration_timestamp': current_epoch_time(),
                    'user_device_name': 'pytile Client'
                })
            self._client_confirmed = True

        data = await self.request(
            'post',
            'clients/{0}/sessions'.format(self._client_uuid),
            json={
                'email': self._email,
                'password': self._password
            })

        if not self._user_uuid:
            self._user_uuid = data['result']['user']['user_uuid']
        self._session_expiry = data['result']['session_expiration_timestamp']

        self.tiles = Tile(self.request, self._user_uuid)

    async def request(
            self,
            method: str,
            endpoint: str,
            *,
            headers: dict = None,
            params: dict = None,
            json: dict = None) -> dict:
        """Make a request against AirVisual."""
        if (self._session_expiry
                and self._session_expiry <= current_epoch_time()):
            raise SessionExpiredError('Session has expired; make a new one!')

        url = '{0}/{1}'.format(API_URL_SCAFFOLD, endpoint)

        if not headers:
            headers = {}
        headers.update({
            'Tile_app_id': TILE_APP_ID,
            'Tile_app_version': TILE_APP_VERSION,
            'Tile_client_uuid': self._client_uuid
        })

        async with self._websession.request(method, url, headers=headers,
                                            params=params, json=json) as resp:
            try:
                resp.raise_for_status()
                data = await resp.json()
                return data
            except client_exceptions.ClientError as err:
                raise RequestError(
                    'Error requesting data from {0}: {1}'.format(
                        endpoint, err)) from None
