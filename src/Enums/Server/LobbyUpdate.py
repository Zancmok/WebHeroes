"""
This module defines an enumeration for various lobby update events.

The `LobbyUpdate` enum is used to represent different events that can occur in a lobby, such as the creation of a new lobby, the addition of a new user, updates to existing users, and the event when a user leaves the lobby.
"""

from enum import Enum


class LobbyUpdate(Enum):
    """
    Enumeration for events related to lobby updates.

    This Enum class defines different types of events that can be triggered within a lobby context. Each event is represented by a string value.

    Attributes:
        new-lobby (str): Indicates the creation of a new lobby.
        new-user (str): Indicates that a new user has joined the lobby.
        user-updated (str): Indicates that a user in the lobby has been updated.
        user-left (str): Indicates that a user has left the lobby.
    """

    NEW_LOBBY: str = "new-lobby"
    NEW_USER: str = "new-user"
    USER_UPDATED: str = "user-updated"
    USER_LEFT: str = "user-left"
