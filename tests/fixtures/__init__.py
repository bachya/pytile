"""Define general fixtures."""
from time import time

import pytest

from ..const import TILE_CLIENT_UUID, TILE_EMAIL, TILE_USER_UUID


@pytest.fixture()
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
            "last_modified_timestamp": 1529449412870,
        },
    }


@pytest.fixture()
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
                "last_modified_timestamp": 1529444807328,
            },
            "session_start_timestamp": int(time() * 1000),
            "session_expiration_timestamp": int(time() * 1000) + 1000,
            "changes": "EXISTING_ACCOUNT",
        },
    }
