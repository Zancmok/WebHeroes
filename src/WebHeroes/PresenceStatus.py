from enum import Enum


class PresenceStatus(Enum):
    """
    An enumeration representing the possible presence statuses of a user.

    Attributes:
        offline (str): Indicates the user is offline and not currently active.
        online (str): Indicates the user is online and currently active.
    """
    offline: str = 'offline'
    online: str = 'online'
