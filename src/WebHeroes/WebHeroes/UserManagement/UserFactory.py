"""
UserManager.py

Manages user instances, providing methods to retrieve and create users.
"""

from typing import Optional

from Enums.Common.PresenceStatus import PresenceStatus
from WebHeroes.UserManagement.User import User
from ZancmokLib.StaticClass import StaticClass


class UserFactory(StaticClass):
    """
    A static class that manages users.

    This class maintains a dictionary of users indexed by their unique user IDs.
    It provides methods to retrieve and create users.
    """

    _users: dict[int, User] = {}
    _user_session_map: dict[int, str] = {}

    @staticmethod
    def get(user_id: int) -> Optional[User]:
        """
        Retrieves a user by their ID.

        :param user_id: The unique identifier of the user.
        :return: The User instance if found, otherwise None.
        """

        return UserFactory._users.get(user_id)

    @staticmethod
    def get_session_id(user_id: int) -> Optional[str]:
        """
        # TODO: Write Docstring!
        """

        if user_id in UserFactory._user_session_map:
            return UserFactory._user_session_map[user_id]

        return None

    @staticmethod
    def assign_session_id(user_id: int, session_id: str) -> None:
        """
        # TODO: Write Docstring!
        """

        UserFactory._user_session_map[user_id] = session_id

    @staticmethod
    def create_user(user_id: int, name: str, avatar_url: str,
                    presence_status: PresenceStatus = PresenceStatus.OFFLINE) -> User:
        """
        Creates a new user and adds them to the user dictionary.

        :param user_id: The unique identifier for the new user.
        :param name: The display name of the user.
        :param avatar_url: The URL of the user's avatar.
        :param presence_status: The initial presence status of the user (default: offline).
        :return: The newly created User instance.
        """

        new_user: User = User(
            user_id=user_id,
            name=name,
            avatar_url=avatar_url,
            presence_status=presence_status
        )

        UserFactory._users[user_id] = new_user

        return new_user
