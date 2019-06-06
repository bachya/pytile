"""Define general fixtures."""
from time import time

import pytest

from ..const import (
    TILE_CLIENT_UUID,
    TILE_EMAIL,
    TILE_TILE_NAME,
    TILE_TILE_UUID,
    TILE_USER_UUID,
)


@pytest.fixture(scope="module")
def fixture_tile_details():
    """Return a /tiles response."""
    return {
        "version": 1,
        "revision": 1,
        "timestamp": "2018-06-19T23:04:39.097Z",
        "timestamp_ms": 1529449479097,
        "result_code": 0,
        "result": {
            TILE_TILE_UUID: {
                "thumbnailImage": "https://local-tile-pub.s3.amazonaws.com/..",
                "tileState": {
                    "ringStateCode": 0,
                    "connectionStateCode": 0,
                    "uuid": TILE_TILE_UUID,
                    "tile_uuid": TILE_TILE_UUID,
                    "client_uuid": TILE_CLIENT_UUID,
                    "timestamp": 1512615215149,
                    "advertised_rssi": 1.4e-45,
                    "client_rssi": 1.4e-45,
                    "battery_level": 1.4e-45,
                    "latitude": 21.9083423,
                    "longitude": -72.4982138,
                    "altitude": 1821.129812,
                    "h_accuracy": 5.0,
                    "v_accuracy": 3.0,
                    "speed": 1.4e-45,
                    "course": 1.4e-45,
                    "authentication": None,
                    "owned": True,
                    "has_authentication": None,
                    "lost_timestamp": -1,
                    "connection_client_uuid": TILE_CLIENT_UUID,
                    "connection_event_timestamp": 1512615234268,
                    "last_owner_update": 1512615215149,
                    "connection_state": "READY",
                    "ring_state": "STOPPED",
                    "is_lost": False,
                    "voip_state": "OFFLINE",
                },
                "entityName": "TILE",
                "tile_uuid": "19264d2dffdbca32",
                "firmware_version": "01.12.14.0",
                "owner_user_uuid": "2ea56f4d-6576-4b4e-af11-3410cc65e373",
                "name": TILE_TILE_NAME,
                "category": None,
                "image_url": "https://local-tile-pub.s3.amazonaws.com/...",
                "visible": True,
                "is_dead": False,
                "hw_version": "02.09",
                "product": "DUTCH1",
                "archetype": "WALLET",
                "configuration": {"fw10_advertising_interval": None},
                "last_tile_state": {
                    "ringStateCode": 0,
                    "connectionStateCode": 0,
                    "uuid": "19264d2dffdbca32",
                    "tile_uuid": "19264d2dffdbca32",
                    "client_uuid": "a01bf97a-c89a-40e2-9534-29976010fb03",
                    "timestamp": 1512615215149,
                    "advertised_rssi": 1.4e-45,
                    "client_rssi": 1.4e-45,
                    "battery_level": 1.4e-45,
                    "latitude": 39.797571,
                    "longitude": -104.887826,
                    "altitude": 1588.002773,
                    "h_accuracy": 5.0,
                    "v_accuracy": 3.0,
                    "speed": 1.4e-45,
                    "course": 1.4e-45,
                    "authentication": None,
                    "owned": True,
                    "has_authentication": None,
                    "lost_timestamp": -1,
                    "connection_client_uuid": TILE_CLIENT_UUID,
                    "connection_event_timestamp": 1512615234268,
                    "last_owner_update": 1512615215149,
                    "connection_state": "DISCONNECTED",
                    "ring_state": "STOPPED",
                    "is_lost": False,
                    "voip_state": "OFFLINE",
                },
                "firmware": {
                    "expected_firmware_version": "",
                    "expected_firmware_imagename": "",
                    "expected_firmware_urlprefix": "",
                    "expected_firmware_publish_date": 0,
                    "expected_ppm": None,
                    "expected_advertising_interval": None,
                    "security_level": 1,
                    "expiry_timestamp": 1529471079097,
                    "expected_tdt_cmd_config": None,
                },
                "auth_key": "aliuUAS7da980asdHJASDQ==",
                "renewal_status": "LEVEL1",
                "metadata": {},
                "auto_retile": False,
                "status": "ACTIVATED",
                "tile_type": "TILE",
                "registration_timestamp": 1482711833983,
                "is_lost": False,
                "auth_timestamp": 1512287015405,
                "activation_timestamp": 1482711835011,
                "last_modified_timestamp": 1514353410254,
            }
        },
    }


@pytest.fixture(scope="module")
def fixture_tile_list():
    """Return a /users/<USER ID>/user_tiles response."""
    return {
        "version": 1,
        "revision": 1,
        "timestamp": "2018-06-19T23:04:32.442Z",
        "timestamp_ms": 1529449472442,
        "result_code": 0,
        "result": [
            {
                "tileType": "TILE",
                "user_uuid": TILE_USER_UUID,
                "tile_uuid": TILE_TILE_UUID,
                "other_user_uuid": "",
                "other_user_email": TILE_EMAIL,
                "mode": "OWNER",
                "last_modified_timestamp": 1482711833985,
            }
        ],
    }


@pytest.fixture(scope="module")
def fixture_expired_session():
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
