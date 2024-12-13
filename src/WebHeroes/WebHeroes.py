from flask import Flask, render_template, request, session, redirect, jsonify
from werkzeug import Response
from zenora import APIClient
from zenora.models.oauth import OauthResponse
from zenora.models.user import OwnUser
from zenora.exceptions import APIError
import WebHeroes.config as config
from WebHeroes.RouteManager import RouteManager
from WebHeroes.LobbyManager import LobbyManager


class WebHeroes:
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

        RouteManager.init(WebHeroes.app)

        WebHeroes.app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY

        WebHeroes.app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG
        )

    @staticmethod
    @app.route("/", methods=["GET"])
    def home() -> str:
        return render_template("index.html")

    @staticmethod
    @app.route("/modding-documentation/")
    def modding_documentation() -> str:
        return render_template("modding-documentation.html")

    @staticmethod
    @app.route("/oauth/", methods=["GET"])
    def oauth() -> Response:
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

        return redirect("/online-lobbies/")

    @staticmethod
    @app.route("/online-lobbies/", methods=["GET"])
    def online_lobbies() -> str | Response:
        if not session.get('access_token', ''):
            return redirect(config.DISCORD_OAUTH_URL)
        
        return render_template("online-lobbies.html")
