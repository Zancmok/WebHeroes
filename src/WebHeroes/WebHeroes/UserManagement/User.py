"""
User.py

This module defines the `User` class, which represents a user in the application.
Each user has an ID, a name, an avatar URL, and a presence status.

Classes:
    User: Represents a user with attributes like ID, name, avatar URL, and presence status.

Usage:
    from WebHeroes.User import User
    from WebHeroes.PresenceStatus import PresenceStatus

    new_user = User(user_id=123, name="Alice")
    print(new_user)
"""

from WebHeroes.UserManagement.EUserPresenceStatus import EUserPresenceStatus


class User:
    """
    Represents a user in the application.

    Attributes:
        user_id (int): A unique identifier for the user.
        name (str): The display name of the user.
        presence_status (EUserPresenceStatus): The user's current presence status,
                                          defaulting to 'offline'.

    Methods:
        __str__(): Returns a concise string representation of the user (ID and name).
    """
    def __init__(self, user_id: int, name: str, presence_status: EUserPresenceStatus = EUserPresenceStatus.OFFLINE) -> None:
        self.user_id: int = user_id
        self.name: str = name
        self.presence_status: EUserPresenceStatus = presence_status

    def __str__(self) -> str:
        return f"User(id:{self.user_id};name:{self.name})"
