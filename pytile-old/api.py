"""Define a base object for interacting with the Tile API."""

import requests

import pytile.const as const
import pytile.exceptions as exceptions
import pytile.util as util


class BaseAPI(object):
    """Define a class that represents an API request."""

    def __init__(self, client_uuid, session):
        """Initialize."""
        self.client_uuid = client_uuid
        self.session = session

    def request(self, method_type, url, **kwargs):
        """Define a generic request."""
        kwargs.setdefault('headers', {})
        kwargs['headers'] = util.merge_two_dicts(
            kwargs['headers'], {
                'Tile_app_id': const.TILE_APP_ID,
                'Tile_app_version': const.TILE_APP_VERSION,
                'Tile_client_uuid': self.client_uuid
            })

        full_url = '{0}/{1}'.format(const.TILE_API_BASE_URL, url)
        method = getattr(self.session, method_type)
        resp = method(full_url, **kwargs)

        # I don't think it's good form to make end users of pytile have to
        #  explicitly catch exceptions from a sub-library, so here, I wrap the
        # Requests HTTPError in my own:
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as exc_info:
            raise exceptions.HTTPError(str(exc_info)) from None

        return resp

    def get(self, url, **kwargs):
        """Define a generic GET request."""
        return self.request('get', url, **kwargs)

    def post(self, url, **kwargs):
        """Define a generic POST request."""
        return self.request('post', url, **kwargs)

    def put(self, url, **kwargs):
        """Define a generic PUT request."""
        return self.request('put', url, **kwargs)
