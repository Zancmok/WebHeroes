"""
Room.py

Defines the Room class, which represents a chat room where users can join and leave.
"""

from WebHeroes.User import User


class Room:
    """
    Represents a chat room where users can be added or removed.

    A Room instance maintains a list of users currently in the room.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.children: list[User] = []

    def add(self, child: User) -> None:
        """
        Adds a user to the room.

        :param child: The User instance representing the user to be added.
        :return: None
        """

        self.children.append(child)

    def remove(self, child: User) -> None:
        """
        Removes a user from the room.

        :param child: The User instance representing the user to be removed.
        :return: None
        """

        self.children.remove(child)
