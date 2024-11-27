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

    def __init__(self) -> None:
        """
        Runs the static WebHeroes.app Flask App.
        """
        WebHeroes.app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

    @staticmethod
    @app.route("/")
    def home() -> str:
        """
        Invokes on main page visit.

        :return: Returns the rendered main page.
        """
        return render_template("index.html")
