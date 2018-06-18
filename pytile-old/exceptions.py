"""Define module exceptions."""


class HTTPError(Exception):
    """Define a generic HTTP error (i.e., a wrapper for Requests)."""
    pass

class MissingUUID(Exception):
    """Define a exception to be raised when a request UUID is missing."""
    pass
