"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import
import json
import re

import aiohttp
import pytest

from pytile import async_login
from pytile.errors import RequestError

from .const import TILE_CLIENT_UUID, TILE_EMAIL, TILE_PASSWORD, TILE_USER_UUID
from .fixtures import *  # noqa


@pytest.mark.asyncio
async def test_bad_endpoint(
    aresponses, event_loop, fixture_create_client, fixture_create_session
):
    """Test that an exception is raised on a bad endpoint."""
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}",
        "put",
        aresponses.Response(text=json.dumps(fixture_create_client), status=200),
    )
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}/sessions",
        "post",
        aresponses.Response(text=json.dumps(fixture_create_session), status=200),
    )
    aresponses.add(
        "production.tile-api.com",
        "/api/v1/bad_endpoint",
        "get",
        aresponses.Response(text="", status=404),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = await async_login(
                TILE_EMAIL, TILE_PASSWORD, websession, client_uuid=TILE_CLIENT_UUID
            )
            await client._request("get", "bad_endpoint")


@pytest.mark.asyncio
async def test_login(
    aresponses, event_loop, fixture_create_client, fixture_create_session
):
    """Test initializing a client with a Tile session."""
    client_pattern = re.compile(r"/api/v1/clients/.+")
    session_pattern = re.compile(r"/api/v1/clients/.+/sessions")

    aresponses.add(
        "production.tile-api.com",
        client_pattern,
        "put",
        aresponses.Response(text=json.dumps(fixture_create_client), status=200),
    )
    aresponses.add(
        "production.tile-api.com",
        session_pattern,
        "post",
        aresponses.Response(text=json.dumps(fixture_create_session), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_login(TILE_EMAIL, TILE_PASSWORD, websession)
        assert isinstance(client.client_uuid, str)
        assert client.client_uuid != TILE_CLIENT_UUID
        assert client.user_uuid == TILE_USER_UUID


@pytest.mark.asyncio
async def test_login_existing(
    aresponses, event_loop, fixture_create_client, fixture_create_session
):
    """Test the creation of a client with an existing client UUID."""
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}",
        "put",
        aresponses.Response(text=json.dumps(fixture_create_client), status=200),
    )
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}/sessions",
        "post",
        aresponses.Response(text=json.dumps(fixture_create_session), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_login(
            TILE_EMAIL, TILE_PASSWORD, websession, client_uuid=TILE_CLIENT_UUID
        )
        assert client.client_uuid == TILE_CLIENT_UUID
