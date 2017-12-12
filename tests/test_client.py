"""Define a set of base API tests."""

# pylint: disable=wildcard-import,redefined-outer-name,unused-wildcard-import

import json
import re

import pytest
import requests_mock

import pytile
from pytile.const import TILE_API_BASE_URL
from tests.fixtures.client import *  # noqa

UUID_PATTERN = r'[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}'
CLIENT_URL_PATTERN = '{0}/clients/{1}'.format(TILE_API_BASE_URL, UUID_PATTERN)
SESSION_URL_PATTERN = '{0}/clients/{1}/sessions'.format(
    TILE_API_BASE_URL, UUID_PATTERN)


def test_bad_credentials(client_response_200):
    """Test what happens when a bad email/password is given."""
    with requests_mock.Mocker() as mock:
        mock.put(
            re.compile(CLIENT_URL_PATTERN),
            text=json.dumps(client_response_200))
        mock.post(
            re.compile(SESSION_URL_PATTERN),
            status_code=401)

        with pytest.raises(pytile.exceptions.HTTPError) as exc_info:
            pytile.Client('email@address.com', 'password12345')
            assert '401' in str(exc_info)


def test_basic_client(client_response_200, session_response_200, user_uuid):
    """Test the creation of a client."""
    with requests_mock.mock() as mock:
        mock.put(
            re.compile(CLIENT_URL_PATTERN),
            text=json.dumps(client_response_200))
        mock.post(
            re.compile(SESSION_URL_PATTERN),
            text=json.dumps(session_response_200))

        client = pytile.Client('email@address.com', 'password12345')
        assert client.user_uuid == user_uuid


def test_client_with_uuid(client_response_200, session_response_200,
                          client_uuid, user_uuid):
    """Test the creation of a client with an existing client UUID."""
    with requests_mock.mock() as mock:
        mock.put(
            re.compile(CLIENT_URL_PATTERN),
            text=json.dumps(client_response_200))
        mock.post(
            re.compile(SESSION_URL_PATTERN),
            text=json.dumps(session_response_200))

        client = pytile.Client(
            'email@address.com', 'password12345', client_uuid=client_uuid)
        assert client.client_uuid == client_uuid
        assert client.user_uuid == user_uuid


def test_get_tiles(tile_active_response_200, tile_list_response_200,
                   client_response_200, session_response_200, user_uuid):
    """Test getting a list of tiles back."""
    with requests_mock.mock() as mock:
        mock.put(
            re.compile(CLIENT_URL_PATTERN),
            text=json.dumps(client_response_200))
        mock.post(
            re.compile(SESSION_URL_PATTERN),
            text=json.dumps(session_response_200))
        mock.get(
            '{0}/users/{1}/user_tiles'.format(TILE_API_BASE_URL, user_uuid),
            text=json.dumps(tile_list_response_200))
        mock.get(
            '{0}/tiles'.format(TILE_API_BASE_URL),
            text=json.dumps(tile_active_response_200))

        client = pytile.Client('email@address.com', 'password12345')
        assert client.user_uuid == user_uuid

        tiles = client.get_tiles()
        assert len(tiles) == len(tile_list_response_200['result'])
