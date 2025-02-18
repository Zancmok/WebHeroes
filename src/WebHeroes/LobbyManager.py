"""
LobbyManager.py

This module defines the `LobbyManager` class, which manages lobby-related routes for a Flask application.
The class uses a `RouteManager` instance to dynamically register routes with the Flask app and provides
static methods for handling user-related requests in the lobby context.

Classes:
    LobbyManager: A static class for managing lobby-related routes and user data.
"""

from flask import session, redirect, request
from flask_socketio import emit, join_room, leave_room
from WebHeroes.RouteManager import RouteManager
from WebHeroes.User import User
from WebHeroes.UserManager import UserManager
from ZancmokLib.StaticClass import StaticClass
from typing import Optional, Any
from WebHeroes.PresenceStatus import PresenceStatus
from WebHeroes.Room import Room
from WebHeroes.LobbyUpdate import LobbyUpdate


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
    other_lobbies: list[Room] = []

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
    @route_manager.event("get-lobby-data")
    def get_lobby_data() -> None:
        """
        Fetches and emits the current lobby data, including the details of the user requesting it,
        the list of users in the current lobby, and other available lobbies with their members.

        The function first checks if the session contains a valid access token. If not, it emits an
        empty lobby data object. Otherwise, it retrieves the user details for the current user (based
        on their user ID stored in the session) and collects the necessary data for the lobby and users.

        The emitted data includes:
        - The current user's details (name, avatar, user ID, and presence status).
        - The details of other users in the same lobby (name, avatar, user ID, and presence status).
        - A list of other available lobbies and their members, with each member's name, avatar, user ID,
        and presence status.

        Emits:
            - Event "get-lobby-data" with a JSON object containing:
                - `self`: The current user's details.
                - `users`: A list of users in the current lobby.
                - `lobbies`: A list of other lobbies with their members' details.
        """

        if not session.get("access_token"):
            emit("get-lobby-data", {}, to=session['user_sid'])

        own_user: User = UserManager.get(session['user_id'])

        emit("get-lobby-data", {
            "self": {
                "name": own_user.name,
                "avatar_url": own_user.avatar_url,
                "user_id": own_user.user_id,
                "presence_status": str(own_user.presence_status)
            },
            "users": [
                {
                    "name": user.name,
                    "avatar_url": user.avatar_url,
                    "user_id": user.user_id,
                    "presence_status": str(user.presence_status)
                } for user in LobbyManager.lobby_room.children
            ],
            "lobbies": [
                {
                    "name": lobby.name,
                    "room_id": lobby.room_id,
                    "owner": {
                        "name": lobby.owner.name,
                        "avatar_url": lobby.owner.avatar_url,
                        "user_id": lobby.owner.user_id,
                        "presence_status": str(lobby.owner.presence_status)
                    },
                    "members": [
                        {
                            "name": member.name,
                            "avatar_url": member.avatar_url,
                            "user_id": member.user_id,
                            "presence_status": str(member.presence_status)
                        } for member in lobby.children
                    ]
                } for lobby in LobbyManager.other_lobbies
            ]
        }, to=session['user_sid'])

    @staticmethod
    @route_manager.event('create-lobby')
    def create_lobby(name: Any) -> None:
        """
        # TODO: Make Docstring
        """

        if not session.get("access_token"):
            emit("create-lobby", {}, to=session['user_sid'])
            return

        # TODO: Make check so only 1 lobby per cyka

        if not name or not type(name) is str:  # TODO: Do better naming limits
            emit("create-lobby", {}, to=session['user_sid'])
            return

        new_lobby: Room = Room(name=name)

        new_lobby.owner = UserManager.get(session['user_id'])
        new_lobby.add(new_lobby.owner)

        LobbyManager.other_lobbies.append(new_lobby)

        LobbyManager.fire_lobby_update(LobbyUpdate.new_lobby, {
            "name": new_lobby.name,
            "room_id": new_lobby.room_id,
            "owner": {
                "name": new_lobby.owner.name,
                "avatar_url": new_lobby.owner.avatar_url,
                "user_id": new_lobby.owner.user_id,
                "presence_status": str(new_lobby.owner.presence_status)
            },
            "members": [
                {
                    "name": member.name,
                    "avatar_url": member.avatar_url,
                    "user_id": member.user_id,
                    "presence_status": str(member.presence_status)
                } for member in new_lobby.children
            ]
        })
        # TODO: Redirect to GET '/lobby/<lobby_id:int>'
        # redirect("")

    @staticmethod
    def fire_lobby_update(reason: LobbyUpdate, change: dict[str, Any]) -> None:
        """
        # TODO: Make Docstring
        """

        emit(
            'lobby-update',
            {
                'reason': str(reason),
                'change': change
            },
            namespace=LobbyManager.lobby_room
        )

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

        session['user_sid'] = request.sid

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

        user: Optional[User] = UserManager.get(session['user_id'])

        if user:
            user.presence_status = PresenceStatus.offline
            LobbyManager.leave_room(
                room=LobbyManager.lobby_room,
                user=user
            )
