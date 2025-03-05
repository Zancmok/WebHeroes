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
        new_lobby (str): Indicates the creation of a new lobby.
        new_user (str): Indicates that a new user has joined the lobby.
        user_updated (str): Indicates that a user in the lobby has been updated.
        user_left (str): Indicates that a user has left the lobby.
    """

    new_lobby: str = "new_lobby"
    new_user: str = "new_user"
    user_updated: str = "user_updated"
    user_left: str = "user_left"
