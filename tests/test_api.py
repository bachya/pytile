"""Define tests for the client object."""
import re
from time import time
from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from pytile import async_login
from pytile.errors import InvalidAuthError, RequestError

from .common import (
    TILE_CLIENT_UUID,
    TILE_EMAIL,
    TILE_PASSWORD,
    TILE_TILE_UUID,
    TILE_USER_UUID,
)


@pytest.mark.asyncio
async def test_bad_endpoint(
    aresponses: ResponsesMockServer,
    authenticated_tile_api_server: ResponsesMockServer,
) -> None:
    """Test that an exception is raised on a bad endpoint.

    Args:
        aresponses: An aresponses server.
        authenticated_tile_api_server: A mock Tile API server connection.
    """
    async with authenticated_tile_api_server:
        authenticated_tile_api_server.add(
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
                await api._async_request(  # pylint: disable=protected-access
                    "get", "bad_endpoint"
                )

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_expired_session(  # pylint: disable=too-many-arguments
    aresponses: ResponsesMockServer,
    authenticated_tile_api_server: ResponsesMockServer,
    create_client_response: dict[str, Any],
    create_session_response: dict[str, Any],
    tile_details_response: dict[str, Any],
    tile_states_response: dict[str, Any],
) -> None:
    """Test that an expired session is recreated automatically.

    Args:
        aresponses: An aresponses server.
        authenticated_tile_api_server: A mock Tile API server connection.
        create_client_response: An API response payload.
        create_session_response: An API response payload.
        tile_details_response: An API response payload.
        tile_states_response: An API response payload.
    """
    async with authenticated_tile_api_server:
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/clients/{TILE_CLIENT_UUID}",
            "put",
            response=aiohttp.web_response.json_response(
                create_client_response, status=200
            ),
        )
        authenticated_tile_api_server.add(
            "production.tile-api.com",
            f"/api/v1/clients/{TILE_CLIENT_UUID}/sessions",
            "post",
            response=aiohttp.web_response.json_response(
                create_session_response, status=200
            ),
        )
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

            # Simulate an expired session:
            api._session_expiry = (  # pylint: disable=protected-access
                int(time() * 1000) - 1000000
            )
            await api.async_get_tiles()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_invalid_auth(aresponses: ResponsesMockServer) -> None:
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

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_login(
    aresponses: ResponsesMockServer,
    authenticated_tile_api_server: ResponsesMockServer,
) -> None:
    """Test initializing a client with a Tile session.

    Args:
        aresponses: An aresponses server.
        authenticated_tile_api_server: A mock Tile API server connection.
    """
    async with authenticated_tile_api_server, aiohttp.ClientSession() as session:
        api = await async_login(TILE_EMAIL, TILE_PASSWORD, session)
        assert isinstance(api.client_uuid, str)
        assert api.client_uuid != TILE_CLIENT_UUID
        assert api.user_uuid == TILE_USER_UUID

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_login_existing(
    aresponses: ResponsesMockServer,
    authenticated_tile_api_server: ResponsesMockServer,
) -> None:
    """Test the creation of a client with an existing client UUID.

    Args:
        aresponses: An aresponses server.
        authenticated_tile_api_server: A mock Tile API server connection.
    """
    async with authenticated_tile_api_server, aiohttp.ClientSession() as session:
        api = await async_login(
            TILE_EMAIL, TILE_PASSWORD, session, client_uuid=TILE_CLIENT_UUID
        )
        assert api.client_uuid == TILE_CLIENT_UUID

    aresponses.assert_plan_strictly_followed()
