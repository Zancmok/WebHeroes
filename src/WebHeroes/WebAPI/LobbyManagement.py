from types import NoneType
from typing import Optional

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
    @route_blueprint.route("/get-data", methods=[EHTTPMethod.POST])
    @FlaskUtil.require_auth()
    def get_data() -> tuple[Response, HTTPCode]:
        raise NotImplementedError

    @staticmethod
    @route_blueprint.route("/create-lobby", methods=[EHTTPMethod.POST])
    @FlaskUtil.require_auth()
    @FlaskUtil.reroute_arguments(lobby_name=str, token=[str, NoneType])
    def create_lobby(lobby_name: str, token: Optional[str]) -> tuple[Response, HTTPCode]:
        ...
