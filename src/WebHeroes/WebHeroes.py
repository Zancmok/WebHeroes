from flask import Flask, render_template, request, session, redirect
from werkzeug import Response
from zenora import APIClient
from zenora.models.oauth import OauthResponse
from zenora.models.user import OwnUser
import WebHeroes.config as config


class WebHeroes:
    """
    The main class. The class is static.
    Used as the main connection between the server and the clients.
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
        Runs the static WebHeroes.app Flask App.
        """

        WebHeroes.app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY

        WebHeroes.app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG
        )

    @staticmethod
    @app.route("/")
    def home() -> str:
        return render_template("index.html")

    @staticmethod
    @app.route("/modding-documentation/")
    def modding_documentation() -> str:
        return render_template("modding-documentation.html")

    @staticmethod
    @app.route("/oauth/")
    def oauth() -> Response:
        oauth_code: str = request.args.get('code', '_')

        if oauth_code == '_':
            return redirect("/")

        oauth_response: OauthResponse = WebHeroes.discord_client.oauth.get_access_token(
            code=oauth_code,
            redirect_uri=config.REDIRECT_URI
        )

        access_token: str = oauth_response.access_token

        session['access_token'] = access_token

        """bearer_client: APIClient = APIClient(access_token, bearer=True)

        current_user: OwnUser = bearer_client.users.get_current_user()"""

        return redirect("/online-lobbies/")

    @staticmethod
    @app.route("/online-lobbies/")
    def online_lobbies() -> str | Response:
        if not session.get('access_token', ''):
            return redirect(config.DISCORD_OAUTH_URL)

        bearer_client: APIClient = APIClient(session['access_token'], bearer=True)

        current_user: OwnUser = bearer_client.users.get_current_user()

        return f"<h1>{current_user.username}</h1>"
