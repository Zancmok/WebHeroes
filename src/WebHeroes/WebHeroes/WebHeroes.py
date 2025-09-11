"""
WebHeroes.py

This module defines the `WebHeroes` class, which serves as the main interface for managing the web server,
handling authentication, and providing various routes for the Flask application.

Classes:
    WebHeroes: A static class that configures and manages the Flask web application and its integration
    with the Discord API.
"""

from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO
from werkzeug import Response
from zenora import APIClient
from zenora.exceptions import APIError
from zenora.models.oauth import OauthResponse
from zenora.models.user import OwnUser

import WebHeroes.config as config
from WebHeroes.DatabaseBridge import DatabaseBridge
from WebHeroes.LobbyManager import LobbyManager
from WebHeroes.RouteManager import RouteManager
from ZancmokLib.StaticClass import StaticClass


class WebHeroes(StaticClass):
    """
    The main class that serves as the primary interface between the server and clients.
    It handles the initialization of the Flask application, manages authentication with Discord,
    and provides necessary setup for the web application to function correctly. This class
    also manages the routes for various web pages and features.

    This class should be used to configure and run the web server, initialize the required
    services (like the Discord API client), and serve dynamic content via Flask routes.

    Attributes:
        app: A Flask instance that handles the web server and routing.
        discord_client: An instance of the Discord API client used to interact with the Discord OAuth service.

    Methods:
        run: Initializes and starts the Flask web server.
    """

    app: Flask = Flask(
        __name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH
    )

    socket_io: SocketIO = SocketIO(app)

    discord_client: APIClient = APIClient(
        token=config.DISCORD_BOT_TOKEN,
        client_secret=config.DISCORD_CLIENT_SECRET
    )

    @staticmethod
    def run() -> None:
        """
        Initializes the Flask application and starts the web server. This method must be
        called to start the web application. It also sets up necessary configurations,
        including the session secret key.

        :return: None
        """

        DatabaseBridge.init()

        managers: list[RouteManager] = [
            LobbyManager.route_manager
        ]

        for manager in managers:
            manager.register_routes(WebHeroes.app, WebHeroes.socket_io)

        WebHeroes.app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY

        WebHeroes.socket_io.run(
            WebHeroes.app,
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            use_reloader=False,
            log_output=True
        )

    @staticmethod
    @app.route("/", methods=["GET"])
    def home() -> str:
        """
        Handles requests to the home page ("/").

        :return: The rendered template for the index page.
        """

        return render_template("index.html")

    @staticmethod
    @app.route("/modding-documentation/")
    def modding_documentation() -> str:
        """
        Serves the modding documentation page.

        :return: The rendered template for the modding documentation page.
        """

        return render_template("modding-documentation.html")

    @staticmethod
    @app.route("/oauth/", methods=["GET"])
    def oauth() -> Response:
        """
        Handles Discord OAuth2 authentication. This route exchanges the authorization code for
        an access token and retrieves user details, which are then stored in the session.

        :return: A redirect response to the online lobbies page or the home page in case of failure.
        """

        oauth_code: str = request.args.get('code', '')

        try:
            oauth_response: OauthResponse = WebHeroes.discord_client.oauth.get_access_token(
                code=oauth_code,
                redirect_uri=config.REDIRECT_URI
            )
        except APIError:
            return redirect("/")

        access_token: str = oauth_response.access_token

        bearer_client: APIClient = APIClient(access_token, bearer=True)

        current_user: OwnUser = bearer_client.users.get_current_user()

        session['access_token'] = access_token
        session['username'] = current_user.username
        session['avatar_url'] = current_user.avatar_url
        session['user_id'] = current_user.id

        return redirect("/online-lobbies/")
