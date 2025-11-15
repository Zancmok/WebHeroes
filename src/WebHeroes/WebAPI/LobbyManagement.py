import WebHeroes.config as config
from flask import Blueprint, Response
from ZancmokLib.FlaskUtil import FlaskUtil
from ZancmokLib.EHTTPMethod import EHTTPMethod
from ZancmokLib.EHTTPCode import EHTTPCode, HTTPCode
from ZancmokLib.StaticClass import StaticClass


class LobbyManagement(StaticClass):
    route_blueprint: Blueprint = Blueprint(
        name="WebAPI:LobbyManagement",
        import_name=__name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH,
        url_prefix="/lobby-management"
    )

    @staticmethod
    @route_blueprint.route("/refresh", methods=[EHTTPMethod.POST])
    @FlaskUtil.require_auth()
    def refresh() -> tuple[Response, HTTPCode]:
        raise NotImplementedError
