"""
LobbyManager.py

This module defines the `LobbyManager` class, which manages lobby-related routes for a Flask application.
The class uses a `RouteManager` instance to dynamically register routes with the Flask app and provides
static methods for handling user-related requests in the lobby context.

Classes:
    LobbyManager: A static class for managing lobby-related routes and user data.
"""

from flask import session
from flask_socketio import emit
from WebHeroes.RouteManager import RouteManager
from WebHeroes.User import User
from ZLib.StaticClass import StaticClass


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
    users: list[User] = []

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
