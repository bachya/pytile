"""Define common test utilities."""
import os

TILE_CLIENT_UUID = "2cc56adc-b96a-4293-9b94-eda716e0aa17"
TILE_EMAIL = "user@email.com"
TILE_PASSWORD = "12345"
TILE_TILE_NAME = "Wallet"
TILE_TILE_UUID = "19264d2dffdbca32"
TILE_USER_UUID = "fd0c10a5-d0f7-4619-9bce-5b2cb7a6754b"


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
