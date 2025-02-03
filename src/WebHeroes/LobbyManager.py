"""
LobbyManager.py

This module defines the `LobbyManager` class, which manages lobby-related routes for a Flask application.
The class uses a `RouteManager` instance to dynamically register routes with the Flask app and provides
static methods for handling user-related requests in the lobby context.

Classes:
    LobbyManager: A static class for managing lobby-related routes and user data.
"""

from flask import session
from flask_socketio import emit, join_room, leave_room
from WebHeroes.RouteManager import RouteManager
from WebHeroes.User import User
from WebHeroes.UserManager import UserManager
from ZLib.StaticClass import StaticClass
from typing import Optional
from WebHeroes.PresenceStatus import PresenceStatus
from WebHeroes.Room import Room


class LobbyManager(StaticClass):
    """
    A class that manages lobby-related routes for a Flask application.

    This class inherits from `StaticClass` and provides static methods for managing routes
    related to user data within the lobby context. It uses a `RouteManager` instance to
    register routes with the Flask app.

    Attributes:
        route_manager (RouteManager): An instance of the RouteManager responsible for
                                      handling route registration for the Flask app.
    """

    route_manager: RouteManager = RouteManager()
    lobby_room: Room = Room("lobby")

    @staticmethod
    def join_room(room: Room, user: User) -> None:
        """
        Adds a user to a chat room.

        This method joins the specified room by its name and adds the user to the room's participant list.

        :param room: The Room instance representing the chat room.
        :param user: The User instance representing the user joining the room.
        :return: None
        """

        join_room(room.name)
        room.add(user)

    @staticmethod
    def leave_room(room: Room, user: User) -> None:
        """
        Removes a user from a chat room.

        This method leaves the specified room by its name and removes the user from the room's participant list.

        :param room: The Room instance representing the chat room.
        :param user: The User instance representing the user leaving the room.
        :return: None
        """

        leave_room(room.name)
        room.remove(user)

    @staticmethod
    @route_manager.event("get-basic-user-data")
    def get_basic_user_data() -> None:
        """
        Emits basic user information stored in the session.

        This function retrieves the username, avatar URL, and user ID of the currently logged-in user
        from the session and emits the data via Socket.IO. If the user is not authenticated (i.e., no
        access token is found in the session), an empty dictionary is emitted instead.

        Emits:
            "get-basic-user-data" (dict): A dictionary containing:
                - username (str): The user's username.
                - avatar_url (str): The URL of the user's avatar.
                - user_id (int): The user's unique ID.

            If the user is not authenticated, an empty dictionary `{}` is emitted.
        """

        if not session.get('access_token'):
            emit("get-basic-user-data", {})
            return

        emit("get-basic-user-data", {
            'username': session['username'],
            'avatar_url': session['avatar_url'],
            'user_id': session['user_id']
        })

    @staticmethod
    @route_manager.event('connect')
    def on_connect() -> Optional[bool]:
        """
        Handles the 'connect' event for a socket connection.

        This method is triggered when a client attempts to establish a socket connection.
        If the client's session does not contain an 'access_token', the connection is rejected
        by returning `False`.

        Returns:
            Optional[bool]: Returns `False` if the 'access_token' is missing in the session;
                            otherwise, no return value is provided (implicitly `None`).
        """

        if not session.get('access_token', ''):
            return False

        if not UserManager.get(session.get('user_id')):
            UserManager.create_user(
                user_id=session['user_id'],
                name=session['username'],
                avatar_url=session['avatar_url'],
                presence_status=PresenceStatus.online
            )
        else:
            user: User = UserManager.get(session['user_id'])

            user.presence_status = PresenceStatus.online

        LobbyManager.join_room(
            room=LobbyManager.lobby_room,
            user=UserManager.get(session['user_id'])
        )

    @staticmethod
    @route_manager.event('disconnect')
    def on_disconnect(reason: str) -> None:
        """
        Handles the 'disconnect' event for a socket connection.

        This method is triggered when a client disconnects from the socket.
        Currently, it is a placeholder and does not perform any actions.

        Args:
            reason (str): A string indicating the reason for the disconnection.
        """

        user: User = UserManager.get(session['user_id'])

        if user:
            user.presence_status = PresenceStatus.offline
            LobbyManager.leave_room(
                room=LobbyManager.lobby_room,
                user=user
            )
