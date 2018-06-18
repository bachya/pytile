"""Define an AirVisual client."""

import requests

import pytile.api as api
import pytile.const as const
import pytile.util as util


class Client(api.BaseAPI):
    """Define an AirVisual API client."""

    def __init__(self, email, password, client_uuid=None, locale='en-US'):
        """Initialize."""
        self._password = password
        self._email = email
        self.locale = locale
        self.session_expiry = None

        if not client_uuid:
            client_uuid = util.generate_uuid()
        self.user_uuid = None

        super(Client, self).__init__(client_uuid, requests.Session())

        self.confirm_client()
        self.create_session()

    @property
    def session_expired(self):
        """Define property that determines whether the session has expired."""
        return (not self.session_expiry
                or self.session_expiry <= util.current_epoch_time())

    def confirm_client(self):
        """Create a (or update an existing) Tile client."""
        self.put(
            'clients/{0}'.format(self.client_uuid),
            data={
                'app_id': const.TILE_APP_ID,
                'app_version': const.TILE_APP_VERSION,
                'locale': self.locale,
                'registration_timestamp': util.current_epoch_time(),
                'user_device_name': 'pytile Client'
            })

    def create_session(self):
        """Create a Tile session."""
        resp = self.post(
            'clients/{0}/sessions'.format(self.client_uuid),
            data={'email': self._email,
                  'password': self._password}).json()

        if not self.user_uuid:
            self.user_uuid = resp['result']['user']['user_uuid']
        self.session_expiry = resp['result']['session_expiration_timestamp']

    def get_tiles(self, type_whitelist=None, show_inactive=False):
        """Get a list of all Tiles owned by the user."""
        # Be nice and create a new session if the current one has expired:
        if self.session_expired:
            self.create_session()

        list_resp = self.get(
            'users/{0}/user_tiles'.format(self.user_uuid)).json()
        tile_uuid_list = [
            tile['tile_uuid'] for tile in list_resp['result']
            if not type_whitelist or tile['tileType'] in type_whitelist
        ]

        tile_resp = self.get(
            'tiles', params={'tile_uuids': tile_uuid_list}).json()
        return [
            tile for tile in tile_resp['result'].values()
            if show_inactive
            or tile['tileState']['connection_state'] == 'READY'
        ]
