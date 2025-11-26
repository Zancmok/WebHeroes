import WebHeroes.config as config
from WebHeroes.LobbyManagement.LobbyManager import LobbyManager
from WebHeroes.Responses import dictify
from WebHeroes.Responses.ResponseTypes.LobbyRefreshResponse import LobbyRefreshResponse
from WebHeroes.Responses.DataModels.MemberModel import MemberModel
from Leek.Repositories.UserRepository import UserRepository
from flask import Blueprint, Response
from flask_socketio import emit
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
        name="WebAPI:LobbyManagement"
    )

    @staticmethod
    @socket_blueprint.on("refresh")
    def refresh() -> None:
        emit("refresh", dictify(LobbyRefreshResponse(
            members=[
                MemberModel(
                    member_id=member_id,
                    member_name=UserRepository.get_by_id(member_id).username
                ) for member_id in LobbyManager.online_lobby.member_ids
            ]
        )))
