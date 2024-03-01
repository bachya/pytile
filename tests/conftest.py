"""Define fixtures, constants, etc. available for all tests."""

import json
import re
from collections.abc import Generator
from time import time
from typing import Any, cast

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from .common import TILE_CLIENT_UUID, TILE_EMAIL, TILE_USER_UUID, load_fixture


@pytest.fixture(name="authenticated_tile_api_server")
def authenticated_tile_api_server_fixture(
    create_client_response: dict[str, Any],
    create_session_response: dict[str, Any],
) -> Generator[ResponsesMockServer, None, None]:
    """Return a fixture that mocks an authenticated tile API server.

    Args:
        create_client_response: An API response payload
        create_session_response: An API response payload
    """
    client_pattern = re.compile(r"/api/v1/clients/.+")
    session_pattern = re.compile(r"/api/v1/clients/.+/sessions")

    server = ResponsesMockServer()
    server.add(
        "production.tile-api.com",
        client_pattern,
        "put",
        response=aiohttp.web_response.json_response(create_client_response, status=200),
    )
    server.add(
        "production.tile-api.com",
        session_pattern,
        "post",
        response=aiohttp.web_response.json_response(
            create_session_response, status=200
        ),
    )
    yield server


@pytest.fixture(name="create_client_response", scope="session")
def create_client_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful client creation payload."""
    return cast(dict[str, Any], json.loads(load_fixture("create_client_response.json")))


@pytest.fixture(name="create_session_response")
def create_session_response_fixture() -> dict[str, Any]:
    """Return a /clients/<UUID>/sessions response.

    Returns:
        An API response payload.
    """
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
                "last_modified_timestamp": 1529444807328,
            },
            "session_start_timestamp": int(time() * 1000),
            "session_expiration_timestamp": int(time() * 1000) + 1000,
            "changes": "EXISTING_ACCOUNT",
        },
    }


@pytest.fixture(name="expired_session_response")
def expired_session_response_fixture() -> dict[str, Any]:
    """Return a /clients/<UUID>/sessions response with an expired session.

    Returns:
        An API response payload.
    """
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
                "last_modified_timestamp": 1529444807328,
            },
            "session_start_timestamp": int(time() * 1000),
            "session_expiration_timestamp": int(time() * 1000) - 1000,
            "changes": "EXISTING_ACCOUNT",
        },
    }


@pytest.fixture(name="tile_details_missing_last_state_response", scope="session")
def tile_details_missing_last_state_response_fixture() -> dict[str, Any]:
    """Return a fixture for a Tile details response that's missing it's state info."""
    return cast(
        dict[str, Any],
        json.loads(load_fixture("tile_details_missing_last_state_response.json")),
    )


@pytest.fixture(name="tile_details_new_name_response_fixture")
def tile_details_new_name_response_fixture() -> dict[str, Any]:
    """Define a fixture for a Tile with a new name.

    Returns:
        An API response payload.
    """
    data = json.loads(load_fixture("tile_details_response.json"))
    data["result"]["name"] = "New Name"
    return cast(dict[str, Any], data)


@pytest.fixture(name="tile_details_response", scope="session")
def tile_details_response_fixture() -> dict[str, Any]:
    """Return a fixture for a Tile details response."""
    return cast(dict[str, Any], json.loads(load_fixture("tile_details_response.json")))


@pytest.fixture(name="tile_details_update_response")
def tile_details_update_response_fixture() -> dict[str, Any]:
    """Define a fixture for a Tile with updated coordinates.

    Returns:
        An API response payload.
    """
    data = json.loads(load_fixture("tile_details_response.json"))
    data["result"]["last_tile_state"]["latitude"] = 51.8943631
    data["result"]["last_tile_state"]["longitude"] = -0.4930538
    return cast(dict[str, Any], data)


@pytest.fixture(name="tile_history_response", scope="session")
def tile_history_response_fixture() -> dict[str, Any]:
    """Return a fixture for a Tile history response."""
    return cast(dict[str, Any], json.loads(load_fixture("tile_history_response.json")))


@pytest.fixture(name="tile_states_response", scope="session")
def tile_states_response_fixture() -> dict[str, Any]:
    """Return a fixture for a Tile states response."""
    return cast(dict[str, Any], json.loads(load_fixture("tile_states_response.json")))
