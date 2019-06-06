"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import

import json

import aiohttp
import pytest

from pytile import Client
from pytile.errors import RequestError

from .const import TILE_CLIENT_UUID, TILE_EMAIL, TILE_PASSWORD, TILE_USER_UUID
from .fixtures import *  # noqa


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
            TILE_EMAIL, TILE_PASSWORD, websession, client_uuid=TILE_CLIENT_UUID
        )
        assert client.client_uuid == TILE_CLIENT_UUID


@pytest.mark.asyncio
async def test_async_init(
    aresponses, event_loop, fixture_create_client, fixture_create_session
):
    """Test initializing a client with a Tile session."""
    aresponses.add(
        "production.tile-api.com",
        "/api/v1/clients/{0}".format(TILE_CLIENT_UUID),
        "put",
        aresponses.Response(text=json.dumps(fixture_create_client), status=200),
    )
    aresponses.add(
        "production.tile-api.com",
        "/api/v1/clients/{0}/sessions".format(TILE_CLIENT_UUID),
        "post",
        aresponses.Response(text=json.dumps(fixture_create_session), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(
            TILE_EMAIL, TILE_PASSWORD, websession, client_uuid=TILE_CLIENT_UUID
        )
        await client.async_init()
        assert client.client_uuid == TILE_CLIENT_UUID
        assert client.user_uuid == TILE_USER_UUID


@pytest.mark.asyncio
async def test_bad_endpoint(aresponses, event_loop):
    """Test that an exception is raised on a bad endpoint."""
    aresponses.add(
        "production.tile-api.com",
        "/api/v1/bad_endpoint",
        "get",
        aresponses.Response(text="", status=404),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(
                TILE_EMAIL, TILE_PASSWORD, websession, client_uuid=TILE_CLIENT_UUID
            )
            await client.request("get", "bad_endpoint")
