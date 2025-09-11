"""
Room.py

Defines the Room class, which represents a chat room where users can join and leave.
The Room class allows management of users in a chat room, including adding and removing users.
"""

from typing import Optional
from WebHeroes.User import User


class Room:
    """
    Represents a chat room where users can join, leave, and manage their participation.

    A Room instance maintains a list of users currently in the room and supports actions such as adding and removing users.
    Each room has a unique ID, a name, and an owner. The owner is typically the user who created the room.

    Attributes:
        name (str): The name of the chat room.
        children (list[User]): A list of users currently in the room.
        owner (Optional[User]): The user who owns the room (if any).
        room_id (int): A unique identifier for the room.
    """

    _id_counter: int = 0

    def __init__(self, name: str) -> None:
        """
        Initializes a new Room instance.

        :param name: The name of the room to be created.
        """

        self.name: str = name
        self.children: list[User] = []
        self.owner: Optional[User] = None
        self.room_id: int = Room._id_counter

        Room._id_counter += 1

    def add(self, child: User) -> None:
        """
        Adds a user to the room.

        This method appends a User instance to the list of users in the room.

        :param child: The User instance representing the user to be added.
        :return: None
        """

        self.children.append(child)

    def remove(self, child: User) -> None:
        """
        Removes a user from the room.

        This method removes a User instance from the list of users in the room.

        :param child: The User instance representing the user to be removed.
        :return: None
        """

        self.children.remove(child)

        if child is self.owner:
            self.owner = None
