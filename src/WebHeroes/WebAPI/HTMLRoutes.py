import WebHeroes.config as config
from ZancmokLib.StaticClass import StaticClass
from ZancmokLib.EHTTPMethod import EHTTPMethod
from ZancmokLib.FlaskUtil import FlaskUtil
from flask import Blueprint, render_template


class HTMLRoutes(StaticClass):
    route_blueprint: Blueprint = Blueprint(
        name="WebAPI:HTMLRoutes",
        import_name=__name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH
    )

    @staticmethod
    @route_blueprint.route("/", methods=[EHTTPMethod.GET])
    def index() -> str:
        """
        Handles requests to the home page ("/").

        :return: The rendered template for the index page.
        """

        return render_template("index.html")

    @staticmethod
    @route_blueprint.route("/modding-documentation/", methods=[EHTTPMethod.GET])
    def modding_documentation() -> str:
        """
        Serves the modding documentation page.

        :return: The rendered template for the modding documentation page.
        """

        return render_template("modding-documentation.html")

    @staticmethod
    @route_blueprint.route("/signup/", methods=[EHTTPMethod.GET])
    def signup() -> str:
        return render_template("signup.html")

    @staticmethod
    @route_blueprint.route("/online-lobbies/", methods=[EHTTPMethod.GET])
    @FlaskUtil.require_auth()
    def online_lobbies() -> str:
        return render_template("online-lobbies.html")

    @staticmethod
    @route_blueprint.route("/lobby/", methods=[EHTTPMethod.GET])
    @FlaskUtil.require_auth()
    def lobby() -> str:
        return render_template("lobby.html")
