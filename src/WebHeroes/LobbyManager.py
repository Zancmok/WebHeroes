from flask import jsonify, session, Response, Flask
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
        if not session.get('access_token'):
            return jsonify({})

        return jsonify(
            {
                'username': session['username'],
                'avatar_url': session['avatar_url'],
                'user_id': session['user_id']
            }
        )
