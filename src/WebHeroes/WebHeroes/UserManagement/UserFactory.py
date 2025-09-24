"""
UserManager.py

Manages user instances, providing methods to retrieve and create users.
"""

from typing import Optional

from WebHeroes.UserManagement.User import User
from ZancmokLib.StaticClass import StaticClass


class UserFactory(StaticClass):
    """
    A static class that manages users.

    This class maintains a dictionary of users indexed by their unique user IDs.
    It provides methods to retrieve and create users.
    """

    _users: dict[int, User] = {}

    @staticmethod
    def get(user_id: int) -> Optional[User]:
        """
        Retrieves a user by their ID.

        :param user_id: The unique identifier of the user.
        :return: The User instance if found, otherwise None.
        """

        user: User = UserFactory._users.get(user_id)
        if user:
            return user

        return None
