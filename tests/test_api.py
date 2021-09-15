"""Define tests for the client object."""
import json
import re
from time import time

import aiohttp
import pytest

from pytile import async_login
from pytile.errors import InvalidAuthError, RequestError

from .common import (
    TILE_CLIENT_UUID,
    TILE_EMAIL,
    TILE_PASSWORD,
    TILE_TILE_UUID,
    TILE_USER_UUID,
    load_fixture,
)


@pytest.mark.asyncio
async def test_bad_endpoint(aresponses, create_session_response):
    """Test that an exception is raised on a bad endpoint."""
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}",
        "put",
        aresponses.Response(
            text=load_fixture("create_client_response.json"), status=200
        ),
    )
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}/sessions",
        "post",
        aresponses.Response(
            text=json.dumps(create_session_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )
    aresponses.add(
        "production.tile-api.com",
        "/api/v1/bad_endpoint",
        "get",
        aresponses.Response(text="", status=404),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as session:
            api = await async_login(
                TILE_EMAIL, TILE_PASSWORD, session, client_uuid=TILE_CLIENT_UUID
            )
            await api.request("get", "bad_endpoint")


@pytest.mark.asyncio
async def test_expired_session(aresponses, create_session_response):
    """Test that an expired session is recreated automatically."""
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}",
        "put",
        aresponses.Response(
            text=load_fixture("create_client_response.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}/sessions",
        "post",
        aresponses.Response(
            text=json.dumps(create_session_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}",
        "put",
        aresponses.Response(
            text=load_fixture("create_client_response.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}/sessions",
        "post",
        aresponses.Response(
            text=json.dumps(create_session_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )
    aresponses.add(
        "production.tile-api.com",
        "/api/v1/tiles/tile_states",
        "get",
        aresponses.Response(
            text=load_fixture("tile_states_response.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/tiles/{TILE_TILE_UUID}",
        "get",
        aresponses.Response(
            text=load_fixture("tile_details_response.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = await async_login(
            TILE_EMAIL, TILE_PASSWORD, session, client_uuid=TILE_CLIENT_UUID
        )

        # Simulate an expired session:
        api._session_expiry = int(time() * 1000) - 1000000
        await api.async_get_tiles()


@pytest.mark.asyncio
async def test_invalid_auth(aresponses):
    """Test initializing a client with a Tile session."""
    client_pattern = re.compile(r"/api/v1/clients/.+")

    aresponses.add(
        "production.tile-api.com",
        client_pattern,
        "put",
        aresponses.Response(
            text="",
            status=401,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(InvalidAuthError):
            await async_login(TILE_EMAIL, TILE_PASSWORD, session)


@pytest.mark.asyncio
async def test_login(aresponses, create_session_response):
    """Test initializing a client with a Tile session."""
    client_pattern = re.compile(r"/api/v1/clients/.+")
    session_pattern = re.compile(r"/api/v1/clients/.+/sessions")

    aresponses.add(
        "production.tile-api.com",
        client_pattern,
        "put",
        aresponses.Response(
            text=load_fixture("create_client_response.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )
    aresponses.add(
        "production.tile-api.com",
        session_pattern,
        "post",
        aresponses.Response(
            text=json.dumps(create_session_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = await async_login(TILE_EMAIL, TILE_PASSWORD, session)
        assert isinstance(api.client_uuid, str)
        assert api.client_uuid != TILE_CLIENT_UUID
        assert api.user_uuid == TILE_USER_UUID


@pytest.mark.asyncio
async def test_login_existing(aresponses, create_session_response):
    """Test the creation of a client with an existing client UUID."""
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}",
        "put",
        aresponses.Response(
            text=load_fixture("create_client_response.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/clients/{TILE_CLIENT_UUID}/sessions",
        "post",
        aresponses.Response(
            text=json.dumps(create_session_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = await async_login(
            TILE_EMAIL, TILE_PASSWORD, session, client_uuid=TILE_CLIENT_UUID
        )
        assert api.client_uuid == TILE_CLIENT_UUID
