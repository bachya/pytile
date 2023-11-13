"""Define tests for the client object."""
import logging
from datetime import datetime
from typing import Any
from unittest.mock import Mock

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from pytile import async_login
from pytile.tile import Tile

from .common import (
    TILE_CLIENT_UUID,
    TILE_EMAIL,
    TILE_PASSWORD,
    TILE_TILE_NAME,
    TILE_TILE_UUID,
)


@pytest.mark.asyncio
async def test_get_history(
    aresponses: ResponsesMockServer,
    authenticated_tile_api_server: ResponsesMockServer,
    tile_details_response: dict[str, Any],
    tile_history_response: dict[str, Any],
    tile_states_response: dict[str, Any],
) -> None:
    """Test getting all Tiles associated with an account.

    Args:
        aresponses: An aresponses server.
        authenticated_tile_api_server: A mock Tile API server connection.
        tile_details_response: An API response payload.
        tile_history_response: An API response payload.
        tile_states_response: An API response payload.
    """
    async with authenticated_tile_api_server:
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            "/api/v1/tiles/tile_states",
            "get",
            response=aiohttp.web_response.json_response(
                tile_states_response, status=200
            ),
        )
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/tiles/{TILE_TILE_UUID}",
            "get",
            response=aiohttp.web_response.json_response(
                tile_details_response, status=200
            ),
        )
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/tiles/location/history/{TILE_TILE_UUID}",
            "get",
            response=aiohttp.web_response.json_response(
                tile_history_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            api = await async_login(
                TILE_EMAIL, TILE_PASSWORD, session, client_uuid=TILE_CLIENT_UUID
            )
            tiles = await api.async_get_tiles()
            tile = tiles[TILE_TILE_UUID]

            start_datetime = datetime(2023, 1, 1, 0, 0, 0)
            end_datetime = datetime(2023, 1, 31, 0, 0, 0)
            history = await tile.async_history(start_datetime, end_datetime)
            assert history == tile_history_response

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_tiles(
    aresponses: ResponsesMockServer,
    authenticated_tile_api_server: ResponsesMockServer,
    tile_details_response: dict[str, Any],
    tile_states_response: dict[str, Any],
) -> None:
    """Test getting all Tiles associated with an account.

    Args:
        aresponses: An aresponses server.
        authenticated_tile_api_server: A mock Tile API server connection.
        tile_details_response: An API response payload.
        tile_states_response: An API response payload.
    """
    async with authenticated_tile_api_server:
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            "/api/v1/tiles/tile_states",
            "get",
            response=aiohttp.web_response.json_response(
                tile_states_response, status=200
            ),
        )
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/tiles/{TILE_TILE_UUID}",
            "get",
            response=aiohttp.web_response.json_response(
                tile_details_response, status=200
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
            assert not tile.lost
            assert tile.firmware_version == "01.12.14.0"
            assert tile.hardware_version == "02.09"
            assert tile.kind == "TILE"
            assert tile.last_timestamp == datetime(2020, 8, 12, 17, 55, 26)
            assert tile.latitude == 51.528308
            assert tile.longitude == -0.3817765
            assert tile.lost_timestamp == datetime(1969, 12, 31, 23, 59, 59, 999000)
            assert tile.name == TILE_TILE_NAME
            assert tile.ring_state == "STOPPED"
            assert tile.uuid == TILE_TILE_UUID
            assert tile.visible
            assert tile.voip_state == "OFFLINE"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_tiles_http_error(
    aresponses: ResponsesMockServer,
    authenticated_tile_api_server: ResponsesMockServer,
    caplog: Mock,
    tile_states_response: dict[str, Any],
) -> None:
    """Test getting all Tiles associated with an account.

    Args:
        aresponses: An aresponses server.
        authenticated_tile_api_server: A mock Tile API server connection.
        caplog: A mocked logging utility.
        tile_states_response: An API response payload.
    """
    caplog.set_level(logging.INFO)

    async with authenticated_tile_api_server:
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            "/api/v1/tiles/tile_states",
            "get",
            response=aiohttp.web_response.json_response(
                tile_states_response, status=200
            ),
        )
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/tiles/{TILE_TILE_UUID}",
            "get",
            response=aresponses.Response(text=None, status=500),
        )

        async with aiohttp.ClientSession() as session:
            api = await async_login(
                TILE_EMAIL, TILE_PASSWORD, session, client_uuid=TILE_CLIENT_UUID
            )
            tiles = await api.async_get_tiles()
            assert len(tiles) == 0
            assert any("Error requesting details" in e.message for e in caplog.records)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_missing_last_tile_state(
    aresponses: ResponsesMockServer,
    authenticated_tile_api_server: ResponsesMockServer,
    tile_details_missing_last_state_response: dict[str, Any],
    tile_states_response: dict[str, Any],
) -> None:
    """Test that a missing last_tile_state is handled correctly.

    Args:
        aresponses: An aresponses server.
        authenticated_tile_api_server: A mock Tile API server connection.
        tile_details_missing_last_state_response: An API response payload.
        tile_states_response: An API response payload.
    """
    async with authenticated_tile_api_server:
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            "/api/v1/tiles/tile_states",
            "get",
            response=aiohttp.web_response.json_response(
                tile_states_response, status=200
            ),
        )
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/tiles/{TILE_TILE_UUID}",
            "get",
            response=aiohttp.web_response.json_response(
                tile_details_missing_last_state_response, status=200
            ),
        )
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/tiles/{TILE_TILE_UUID}",
            "get",
            response=aiohttp.web_response.json_response(
                tile_details_missing_last_state_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            api = await async_login(
                TILE_EMAIL, TILE_PASSWORD, session, client_uuid=TILE_CLIENT_UUID
            )
            tiles = await api.async_get_tiles()
            tile = tiles[TILE_TILE_UUID]
            assert not tile.accuracy
            assert not tile.altitude
            assert not tile.last_timestamp
            assert not tile.latitude
            assert not tile.longitude
            assert tile.lost
            assert not tile.lost_timestamp
            assert not tile.ring_state
            assert not tile.voip_state

            await tile.async_update()
            assert not tile.latitude
            assert not tile.longitude

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_tile_as_dict(
    aresponses: ResponsesMockServer,
    authenticated_tile_api_server: ResponsesMockServer,
    tile_details_response: dict[str, Any],
    tile_states_response: dict[str, Any],
) -> None:
    """Test dumping a Tile as a dictionary.

    Args:
        aresponses: An aresponses server.
        authenticated_tile_api_server: A mock Tile API server connection.
        tile_details_response: An API response payload.
        tile_states_response: An API response payload.
    """
    async with authenticated_tile_api_server:
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            "/api/v1/tiles/tile_states",
            "get",
            response=aiohttp.web_response.json_response(
                tile_states_response, status=200
            ),
        )
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/tiles/{TILE_TILE_UUID}",
            "get",
            response=aiohttp.web_response.json_response(
                tile_details_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            api = await async_login(
                TILE_EMAIL, TILE_PASSWORD, session, client_uuid=TILE_CLIENT_UUID
            )
            tiles = await api.async_get_tiles()
            assert len(tiles) == 1
            tile = tiles[TILE_TILE_UUID]
            assert tile.as_dict() == {
                "accuracy": 13.496111,
                "altitude": 0.4076319168123,
                "archetype": "WALLET",
                "dead": False,
                "firmware_version": "01.12.14.0",
                "hardware_version": "02.09",
                "kind": "TILE",
                "last_timestamp": datetime(2020, 8, 12, 17, 55, 26),
                "latitude": 51.528308,
                "longitude": -0.3817765,
                "lost": False,
                "lost_timestamp": datetime(1969, 12, 31, 23, 59, 59, 999000),
                "name": "Wallet",
                "ring_state": "STOPPED",
                "uuid": "19264d2dffdbca32",
                "visible": True,
                "voip_state": "OFFLINE",
            }

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_tile_label(
    aresponses: ResponsesMockServer,
    authenticated_tile_api_server: ResponsesMockServer,
    tile_states_response: dict[str, Any],
) -> None:
    """Test a Tile label (which is ignored by this library).

    This is a sanity check that a Tile Label, which returns an HTTP 412 when passed to
    /api/v1/tiles/{TILE_UUID}, is handled correctly.

    Args:
        aresponses: An aresponses server.
        authenticated_tile_api_server: A mock Tile API server connection.
        tile_states_response: An API response payload.
    """
    async with authenticated_tile_api_server:
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            "/api/v1/tiles/tile_states",
            "get",
            response=aiohttp.web_response.json_response(
                tile_states_response, status=200
            ),
        )
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/tiles/{TILE_TILE_UUID}",
            "get",
            response=aresponses.Response(text="", status=412),
        )

        async with aiohttp.ClientSession() as session:
            api = await async_login(
                TILE_EMAIL, TILE_PASSWORD, session, client_uuid=TILE_CLIENT_UUID
            )
            tiles = await api.async_get_tiles()
            assert len(tiles) == 0

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_tile_update(
    aresponses: ResponsesMockServer,
    authenticated_tile_api_server: ResponsesMockServer,
    tile_details_response: dict[str, Any],
    tile_details_update_response: dict[str, Any],
    tile_states_response: dict[str, Any],
) -> None:
    """Test updating a Tile's status.

    Args:
        aresponses: An aresponses server.
        authenticated_tile_api_server: A mock Tile API server connection.
        tile_details_response: An API response payload.
        tile_details_update_response: An API response payload.
        tile_states_response: An API response payload.
    """
    async with authenticated_tile_api_server:
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            "/api/v1/tiles/tile_states",
            "get",
            response=aiohttp.web_response.json_response(
                tile_states_response, status=200
            ),
        )
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/tiles/{TILE_TILE_UUID}",
            "get",
            response=aiohttp.web_response.json_response(
                tile_details_response, status=200
            ),
        )
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/tiles/{TILE_TILE_UUID}",
            "get",
            response=aiohttp.web_response.json_response(
                tile_details_update_response, status=200
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

    aresponses.assert_plan_strictly_followed()
