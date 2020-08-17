"""Define fixtures, constants, etc. available for all tests."""
import json
from time import time

import pytest

from .common import TILE_CLIENT_UUID, TILE_EMAIL, TILE_USER_UUID, load_fixture


@pytest.fixture()
def create_session_response():
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
                "last_modified_timestamp": 1529444807328,
            },
            "session_start_timestamp": int(time() * 1000),
            "session_expiration_timestamp": int(time() * 1000) + 1000,
            "changes": "EXISTING_ACCOUNT",
        },
    }


@pytest.fixture()
def expired_session_response():
    """Return a /clients/<UUID>/sessions response with an expired session."""
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


@pytest.fixture()
def tile_details_new_name_response():
    """Define a fixture for a subscription with an ALARM alarm state."""
    raw = load_fixture("tile_details_response.json")
    data = json.loads(raw)
    data["result"]["name"] = "New Name"
    return json.dumps(data)


@pytest.fixture()
def tile_details_update_response():
    """Define a fixture for a subscription with an ALARM alarm state."""
    raw = load_fixture("tile_details_response.json")
    data = json.loads(raw)
    data["result"]["last_tile_state"]["latitude"] = 51.8943631
    data["result"]["last_tile_state"]["longitude"] = -0.4930538
    return json.dumps(data)
