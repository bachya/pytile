"""Define various utility functions."""

import time
import uuid


def generate_uuid():
    """Generate a Tile-compliant UUID."""
    return str(uuid.uuid4())


def merge_two_dicts(dict1, dict2):
    """Combine two dicts into one."""
    final = dict1.copy()
    final.update(dict2)
    return final


def current_epoch_time():
    """Return the number of milliseconds since the Epoch."""
    return int(time.time() * 1000)
