class AlreadyOwningLobbyError(Exception):
    """Raised when trying to create a lobby whilst owning a lobby."""
    pass
