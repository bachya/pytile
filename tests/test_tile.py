"""Define tests for the client object."""
from datetime import datetime
import json

import aiohttp
import pytest

from pytile import async_login
from pytile.tile import Tile

from .common import (
    TILE_CLIENT_UUID,
    TILE_EMAIL,
    TILE_PASSWORD,
    TILE_TILE_NAME,
    TILE_TILE_UUID,
    load_fixture,
)


@pytest.mark.asyncio
async def test_get_tiles(aresponses, create_session_response):
    """Test getting all Tiles associated with an account."""
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
        tiles = await api.async_get_tiles()
        assert len(tiles) == 1
        tile = tiles[TILE_TILE_UUID]
        assert isinstance(tile, Tile)
        assert str(tile) == f"<Tile uuid={TILE_TILE_UUID} name={TILE_TILE_NAME}>"
        assert tile.accuracy == 13.496111
        assert tile.altitude == 0.4076319168123
        assert tile.archetype == "WALLET"
        assert not tile.dead
        assert tile.firmware_version == "01.12.14.0"
        assert tile.hardware_version == "02.09"
        assert tile.kind == "TILE"
        assert tile.last_timestamp == datetime(2020, 8, 12, 11, 55, 26)
        assert tile.latitude == 51.528308
        assert tile.longitude == -0.3817765
        assert not tile.lost
        assert tile.lost_timestamp == datetime(1969, 12, 31, 16, 59, 59, 999000)
        assert tile.name == TILE_TILE_NAME
        assert tile.uuid == TILE_TILE_UUID
        assert tile.visible


@pytest.mark.asyncio
async def test_tile_update(
    aresponses, create_session_response, tile_details_update_response
):
    """Test updating a Tile's status."""
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
    aresponses.add(
        "production.tile-api.com",
        f"/api/v1/tiles/{TILE_TILE_UUID}",
        "get",
        aresponses.Response(
            text=tile_details_update_response,
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = await async_login(
            TILE_EMAIL, TILE_PASSWORD, session, client_uuid=TILE_CLIENT_UUID
        )
        tiles = await api.async_get_tiles()
        tile = tiles[TILE_TILE_UUID]
        assert tile.latitude == 51.528308
        assert tile.longitude == -0.3817765

        await tile.async_update()
        assert tile.latitude == 51.8943631
        assert tile.longitude == -0.4930538
