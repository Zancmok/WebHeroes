from flask import Flask, render_template, request
from zenora import APIClient
from zenora.models.oauth import OauthResponse
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
    def oauth() -> str:
        oauth_code: str = request.args.get('code', '_')

        if oauth_code == '_':
            return render_template("index.html")

        access_token: OauthResponse = WebHeroes.discord_client.oauth.get_access_token(
            code=oauth_code,
            redirect_uri=config.DISCORD_OAUTH_URL
        )

        return ""

    @staticmethod
    @app.route("/online-lobbies/")
    def online_lobbies() -> str:
        print("Darn")
        
        return ""
