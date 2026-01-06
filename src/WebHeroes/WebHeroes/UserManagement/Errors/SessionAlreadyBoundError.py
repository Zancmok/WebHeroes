class SessionAlreadyBoundError(Exception):
    """Raised when trying to bind a session that is already bound to a socket connection."""
    pass
