"""
WebHeroes.py

This module defines the `WebHeroes` class, which serves as the main interface for managing the web server,
handling authentication, and providing various routes for the Flask application.

Classes:
    WebHeroes: A static class that configures and manages the Flask web application and its integration
    with the Discord API.
"""

from flask import Flask, render_template, request, session, redirect
from werkzeug import Response
from zenora import APIClient
from zenora.models.oauth import OauthResponse
from zenora.models.user import OwnUser
from zenora.exceptions import APIError
from ZLib.StaticClass import StaticClass
import WebHeroes.config as config
from WebHeroes.LobbyManager import LobbyManager
from WebHeroes.DatabaseBridge import DatabaseBridge


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

        LobbyManager.route_manager.register_routes(WebHeroes.app)

        WebHeroes.app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY

        WebHeroes.app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG
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

    @staticmethod
    @app.route("/online-lobbies/", methods=["GET"])
    def online_lobbies() -> str | Response:
        """
        Manages the online lobbies route. If the user is not authenticated, they are redirected
        to the Discord OAuth2 authorization page. Otherwise, the online lobbies page is rendered.

        :return: The rendered online lobbies template or a redirect response to the OAuth2 URL.
        """

        if not session.get('access_token', ''):
            return redirect(config.DISCORD_OAUTH_URL)
        
        return render_template("online-lobbies.html")
