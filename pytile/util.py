"""Define various utility functions."""
from time import time


def current_epoch_time() -> int:
    """Return the number of milliseconds since the Epoch."""
    return int(time() * 1000)
