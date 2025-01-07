"""
User.py

This module defines the `User` class, which represents a user in the application.
Each user has an ID, a name, an avatar URL, and a presence status.

Classes:
    User: Represents a user with attributes like ID, name, avatar URL, and presence status.

Usage:
    from WebHeroes.User import User
    from WebHeroes.PresenceStatus import PresenceStatus

    new_user = User(user_id=123, name="Alice", avatar_url="http://example.com/avatar.png")
    print(new_user)
"""

from WebHeroes.PresenceStatus import PresenceStatus


class User:
    """
    Represents a user in the application.

    Attributes:
        user_id (int): A unique identifier for the user.
        name (str): The display name of the user.
        avatar_url (str): The URL to the user's avatar image.
        presence_status (PresenceStatus): The user's current presence status,
                                          defaulting to 'offline'.

    Methods:
        __str__(): Returns a concise string representation of the user (ID and name).
        __repr__(): Returns a detailed string representation of the user (ID, name, and avatar URL).
    """
    def __init__(self, user_id: int, name: str, avatar_url: str, presence_status: PresenceStatus = PresenceStatus.offline) -> None:
        self.user_id: int = user_id
        self.name: str = name
        self.avatar_url: str = avatar_url
        self.presence_status: PresenceStatus = presence_status

    def __str__(self) -> str:
        return f"User(id:{self.user_id};name:{self.name})"

    def __repr__(self) -> str:
        return f"User(id:{self.user_id};name:{self.name};avatar:{self.avatar_url})"
