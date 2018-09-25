"""Define package errors."""


class TileError(Exception):
    """Define a base error."""

    pass


class RequestError(TileError):
    """Define an error related to invalid requests."""

    pass


class SessionExpiredError(TileError):
    """Define an error for when a Tile app session expires."""

    pass
