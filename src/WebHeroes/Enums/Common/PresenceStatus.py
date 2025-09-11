"""
PresenceStatus.py

This module defines the `PresenceStatus` enumeration, representing the possible presence
statuses of a user in the application.

Classes:
    PresenceStatus: An enumeration representing whether a user is online or offline.
"""

from enum import Enum


class PresenceStatus(Enum):
    """
    An enumeration representing the possible presence statuses of a user.

    Attributes:
        OFFLINE (str): Indicates the user is offline and not currently active.
        ONLINE (str): Indicates the user is online and currently active.
    """
    OFFLINE: str = 'offline'
    ONLINE: str = 'online'
