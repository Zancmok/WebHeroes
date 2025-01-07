"""
LobbyManager.py

This module defines the `LobbyManager` class, which manages lobby-related routes for a Flask application.
The class uses a `RouteManager` instance to dynamically register routes with the Flask app and provides
static methods for handling user-related requests in the lobby context.

Classes:
    LobbyManager: A static class for managing lobby-related routes and user data.
"""

from flask import jsonify, session, Response
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
    @route_manager.route("/get-basic-user-data/", methods=['GET'])
    def get_basic_user_data() -> Response:
        """
        Returns basic user information stored in the session.

        This route retrieves the username, avatar URL, and user ID of the currently logged-in user
        from the session. If no access token is present in the session, an empty JSON object is returned.

        :return: A JSON response containing basic user data or an empty JSON object if the user is not authenticated.
        """

        if not session.get('access_token'):
            return jsonify({})

        return jsonify(
            {
                'username': session['username'],
                'avatar_url': session['avatar_url'],
                'user_id': session['user_id']
            }
        )
