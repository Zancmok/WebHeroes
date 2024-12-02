from flask import Flask, render_template
import WebHeroes.config as config


class WebHeroes:
    """
    The main class. The class is static.
    """

    app: Flask = Flask(
        __name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH
    )

    @staticmethod
    def run() -> None:
        """
        Runs the static WebHeroes.app Flask App.
        """
        WebHeroes.app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

    @staticmethod
    @app.route("/")
    def home() -> str:
        return render_template("index.html")

    @staticmethod
    @app.route("/modding-documentation/")
    def modding_documentation() -> str:
        return render_template("modding-documentation.html")
        
    @staticmethod
    @app.route("/online-lobbies/")
    def online_lobbies() -> str:
        print("Darn")
        
        return ""
