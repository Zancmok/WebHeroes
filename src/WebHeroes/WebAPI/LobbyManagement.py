import WebHeroes.config as config
from flask import Blueprint, Response
from ZancmokLib.FlaskUtil import FlaskUtil
from ZancmokLib.EHTTPMethod import EHTTPMethod
from ZancmokLib.EHTTPCode import EHTTPCode, HTTPCode
from ZancmokLib.StaticClass import StaticClass
from ZancmokLib.SocketBlueprint import SocketBlueprint


class LobbyManagement(StaticClass):
    route_blueprint: Blueprint = Blueprint(
        name="WebAPI:LobbyManagement",
        import_name=__name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH,
        url_prefix="/lobby-management"
    )

    socket_blueprint: SocketBlueprint = SocketBlueprint(
        name="lobby/"
    )

    @staticmethod
    @socket_blueprint.on("refresh")
    def refresh() -> None:
        raise NotImplementedError
