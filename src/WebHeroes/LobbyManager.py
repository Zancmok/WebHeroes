"""
LobbyManager.py

This module defines the `LobbyManager` class, which manages lobby-related routes for a Flask application.
The class uses a `RouteManager` instance to dynamically register routes with the Flask app and provides
static methods for handling user-related requests in the lobby context.

Classes:
    LobbyManager: A static class for managing lobby-related routes and user data.
"""

from typing import Optional

from flask import session, request
from flask_socketio import emit, join_room, leave_room

from Enums.Common.PresenceStatus import PresenceStatus
from Enums.Server.LobbyUpdate import LobbyUpdate
from Enums.Server.SocketEvent import SocketEvent
from WebHeroes.ResponseTypes import dictify, GetLobbyDataResponse, UserResponse, LobbyResponse, EmptyResponse, \
    LobbyUpdateResponse, NewUserUpdateResponse, UserLeftUpdateResponse, NewLobbyUpdateResponse, SuccessResponse
from WebHeroes.Room import Room
from WebHeroes.RouteManager import RouteManager
from WebHeroes.User import User
from WebHeroes.UserManager import UserManager
from ZancmokLib.StaticClass import StaticClass


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
    @route_manager.event(SocketEvent.GET_LOBBY_DATA)
    def get_lobby_data() -> None:
        """
        Fetches and emits the current lobby data, providing information about the requesting user,
        the users in the same lobby, and other available lobbies.

        Behavior:
        - If the session lacks a valid access token, an `EmptyResponse` is emitted.
        - Retrieves the requesting user's details based on their session user ID.
        - Gathers information about the current lobby's users.
        - Collects details of other available lobbies and their members.

        Response Types:
        - `EmptyResponse`: If the user is not authenticated.
        - `GetLobbyDataResponse`: If the user is authenticated.
        """

        if not session.get("access_token"):
            emit(SocketEvent.GET_LOBBY_DATA, dictify(EmptyResponse()), to=session["user_session_id"])

        own_user: User = UserManager.get(session['user_id'])

        emit(SocketEvent.GET_LOBBY_DATA,
             dictify(GetLobbyDataResponse(
                 self=UserResponse(
                     user_id=own_user.user_id,
                     username=own_user.name,
                     avatar_url=own_user.avatar_url,
                     presence_status=own_user.presence_status
                 ),
                 users=[UserResponse(
                     user_id=user.user_id,
                     username=user.name,
                     avatar_url=user.avatar_url,
                     presence_status=user.presence_status
                 ) for user in LobbyManager.lobby_room.children],
                 lobbies=[LobbyResponse(
                     room_id=lobby.room_id,
                     name=lobby.name,
                     owner=UserResponse(
                         user_id=lobby.owner.user_id,
                         username=lobby.owner.name,
                         avatar_url=lobby.owner.avatar_url,
                         presence_status=lobby.owner.presence_status
                     ),
                     members=[UserResponse(
                         user_id=member.user_id,
                         username=member.name,
                         avatar_url=member.avatar_url,
                         presence_status=member.presence_status
                     ) for member in lobby.children]
                 ) for lobby in LobbyManager.other_lobbies]
             )),
             to=session["user_session_id"])

    @staticmethod
    @route_manager.event(SocketEvent.CREATE_LOBBY)
    def create_lobby(lobby_name: str) -> None:
        if type(lobby_name) is not str:
            emit(SocketEvent.CREATE_LOBBY, dictify(EmptyResponse()), to=session['user_session_id'])
            return
        
        # TODO: Check if user already made a lobby or is in a lobby already!!!

        new_lobby: Room = Room(lobby_name)
        
        own_user: User = UserManager.get(session['user_id'])

        new_lobby.owner = own_user
        new_lobby.children.append(own_user)

        LobbyManager.leave_room(
            room=LobbyManager.lobby_room,
            user=own_user
        )

        LobbyManager.join_room(
            room=new_lobby,
            user=own_user
        )

        LobbyManager.other_lobbies.append(new_lobby)

        emit(SocketEvent.LOBBY_UPDATE,
             dictify(LobbyUpdateResponse(
                 change_type=LobbyUpdate.new_lobby,
                 change=NewLobbyUpdateResponse(
                     lobby_name=lobby_name,
                     owner=UserResponse(
                         user_id=own_user.user_id,
                         username=own_user.name,
                         avatar_url=own_user.avatar_url,
                         presence_status=own_user.presence_status
                     )
                 )
             )), to=LobbyManager.lobby_room.name)

        emit(SocketEvent.LOBBY_UPDATE,
             dictify(LobbyUpdateResponse(
                 change_type=LobbyUpdate.user_left,
                 change=UserLeftUpdateResponse(
                     user=UserResponse(
                         user_id=own_user.user_id,
                         username=own_user.name,
                         avatar_url=own_user.avatar_url,
                         presence_status=own_user.presence_status
                     )
                 )
             )), to=LobbyManager.lobby_room.name)
        
        emit(SocketEvent.CREATE_LOBBY, dictify(SuccessResponse()), to=session['user_session_id'])

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

        session["user_session_id"] = request.sid

        user: User
        if not UserManager.get(session.get('user_id')):
            UserManager.create_user(
                user_id=session['user_id'],
                name=session['username'],
                avatar_url=session['avatar_url'],
                presence_status=PresenceStatus.online
            )

            user = UserManager.get(session['user_id'])
        else:
            user = UserManager.get(session['user_id'])

            user.presence_status = PresenceStatus.online

        emit(SocketEvent.LOBBY_UPDATE,
             dictify(LobbyUpdateResponse(
                 change_type=LobbyUpdate.new_user,
                 change=NewUserUpdateResponse(
                     user=UserResponse(
                         user_id=user.user_id,
                         username=user.name,
                         avatar_url=user.avatar_url,
                         presence_status=user.presence_status
                     )
                 )
             )), to=LobbyManager.lobby_room.name)

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

        user.presence_status = PresenceStatus.offline
        LobbyManager.leave_room(
            room=LobbyManager.lobby_room,
            user=user
        )

        emit(SocketEvent.LOBBY_UPDATE,
             dictify(LobbyUpdateResponse(
                 change_type=LobbyUpdate.user_left,
                 change=UserLeftUpdateResponse(
                     user=UserResponse(
                         user_id=user.user_id,
                         username=user.name,
                         avatar_url=user.avatar_url,
                         presence_status=user.presence_status
                     )
                 )
             )), to=LobbyManager.lobby_room.name)
