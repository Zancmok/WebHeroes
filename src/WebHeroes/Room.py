"""
Room.py

Defines the Room class, which represents a chat room where users can join and leave.
"""

# TODO: Fix Docstring!!!

from WebHeroes.User import User
from typing import Optional


class Room:
    """
    Represents a chat room where users can be added or removed.

    A Room instance maintains a list of users currently in the room.
    """

    _id_counter: int = 0

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.children: list[User] = []
        self.owner: Optional[User] = None
        self.room_id: int = Room._id_counter

        Room._id_counter += 1

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
