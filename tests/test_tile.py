"""Define tests for the client object."""
import json

import aiohttp
import pytest

from pytile import async_login
from pytile.errors import SessionExpiredError

from .common import (
    TILE_CLIENT_UUID,
    TILE_EMAIL,
    TILE_PASSWORD,
    TILE_TILE_NAME,
    TILE_USER_UUID,
    load_fixture,
)


@pytest.mark.asyncio
async def test_get_all(
    aresponses, fixture_create_session,
):
    """Test getting details on all of a user's tiles."""
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
        aresponses.Response(text=json.dumps(fixture_create_session), status=200),
    )
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/users/{TILE_USER_UUID}/user_tiles",
        "get",
        aresponses.Response(text=load_fixture("tile_list_response.json"), status=200),
    )
    aresponses.add(
        "production.tile-api.com",
        "/api/v1/tiles",
        "get",
        aresponses.Response(
            text=load_fixture("tile_details_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as websession:
        client = await async_login(
            TILE_EMAIL, TILE_PASSWORD, websession, client_uuid=TILE_CLIENT_UUID
        )
        tiles = await client.tiles.all()
        assert tiles[0]["name"] == TILE_TILE_NAME


@pytest.mark.asyncio  # noqa
async def test_expired_session(aresponses, fixture_expired_session):
    """Test raising an exception on an expired session."""
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
        aresponses.Response(text=json.dumps(fixture_expired_session), status=200),
    )

    with pytest.raises(SessionExpiredError):
        async with aiohttp.ClientSession() as websession:
            client = await async_login(
                TILE_EMAIL, TILE_PASSWORD, websession, client_uuid=TILE_CLIENT_UUID
            )
            await client.tiles.all()
