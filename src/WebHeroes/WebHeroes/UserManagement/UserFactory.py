"""
UserManager.py

Manages user instances, providing methods to retrieve and create users.
"""

from typing import Optional
from Leek.Models.UserModel import UserModel
from ZancmokLib.StaticClass import StaticClass


class UserFactory(StaticClass):
    """
    A static class that manages users.

    This class maintains a dictionary of users indexed by their unique user IDs.
    It provides methods to retrieve and create users.
    """

    @staticmethod
    def get(user_id: int) -> Optional[UserModel]:
        """
        Retrieves a user by their ID.

        :param user_id: The unique identifier of the user.
        :return: The User instance if found, otherwise None.
        """

        raise NotImplementedError
