"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import
import json
from time import time

import aiohttp
import pytest

from pytile import Client
from pytile.errors import RequestError

from .const import TILE_CLIENT_UUID, TILE_EMAIL, TILE_PASSWORD, TILE_USER_UUID


@pytest.fixture(scope='session')
def fixture_create_client():
    """Return a /clients/<UUID> response."""
    return {
        "version": 1,
        "revision": 1,
        "timestamp": "2018-06-19T23:03:32.873Z",
        "timestamp_ms": 1529449412873,
        "result_code": 0,
        "result": {
            "locale": "en-US",
            "client_uuid": TILE_CLIENT_UUID,
            "app_id": "ios-tile-production",
            "app_version": "2.31.0",
            "os_name": None,
            "os_release": None,
            "model": None,
            "signed_in_user_uuid": None,
            "registration_timestamp": 1529449412870,
            "user_device_name": None,
            "beta_option": False,
            "last_modified_timestamp": 1529449412870
        }
    }


@pytest.fixture(scope='session')
def fixture_create_session():
    """Return a /clients/<UUID>/sessions response."""
    return {
        "version": 1,
        "revision": 1,
        "timestamp": "2018-06-19T23:04:24.672Z",
        "timestamp_ms": 1529449464672,
        "result_code": 0,
        "result": {
            "client_uuid": TILE_CLIENT_UUID,
            "user": {
                "user_uuid": TILE_USER_UUID,
                "full_name": None,
                "email": TILE_EMAIL,
                "beta_eligibility": False,
                "gift_recipient": True,
                "locale": "en-US",
                "email_shared": True,
                "image_url": None,
                "status": "ACTIVATED",
                "pw_exists": True,
                "linked_accounts": [],
                "registration_timestamp": 1482711582203,
                "last_modified_timestamp": 1529444807328
            },
            "session_start_timestamp": int(time() * 1000),
            "session_expiration_timestamp": int(time() * 1000) + 1000,
            "changes": "EXISTING_ACCOUNT"
        }
    }


# pylint: disable=protected-access
@pytest.mark.asyncio
async def test_create(event_loop):
    """Test the creation of a client."""
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(TILE_EMAIL, TILE_PASSWORD, websession)
        assert client.client_uuid != TILE_CLIENT_UUID


@pytest.mark.asyncio
async def test_create_existing(event_loop):
    """Test the creation of a client with an existing client UUID."""
    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(
            TILE_EMAIL,
            TILE_PASSWORD,
            websession,
            client_uuid=TILE_CLIENT_UUID)
        assert client.client_uuid == TILE_CLIENT_UUID


@pytest.mark.asyncio
async def test_get_session(
        aresponses, event_loop, fixture_create_client, fixture_create_session):
    """Test initializing a client with a Tile session."""
    aresponses.add(
        'production.tile-api.com',
        '/api/v1/clients/{0}'.format(TILE_CLIENT_UUID), 'put',
        aresponses.Response(
            text=json.dumps(fixture_create_client), status=200))
    aresponses.add(
        'production.tile-api.com',
        '/api/v1/clients/{0}/sessions'.format(TILE_CLIENT_UUID), 'post',
        aresponses.Response(
            text=json.dumps(fixture_create_session), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(
            TILE_EMAIL,
            TILE_PASSWORD,
            websession,
            client_uuid=TILE_CLIENT_UUID)
        await client.get_session()
        assert client.client_uuid == TILE_CLIENT_UUID
        assert client.user_uuid == TILE_USER_UUID


@pytest.mark.asyncio
async def test_bad_endpoint(aresponses, event_loop):
    """Test that an exception is raised on a bad endpoint."""
    aresponses.add(
        'production.tile-api.com',
        '/api/v1/bad_endpoint', 'get',
        aresponses.Response(
            text='', status=404))

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(
                TILE_EMAIL,
                TILE_PASSWORD,
                websession,
                client_uuid=TILE_CLIENT_UUID)
            await client.request('get', 'bad_endpoint')
