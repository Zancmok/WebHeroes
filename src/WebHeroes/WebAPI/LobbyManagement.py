from typing import Any
import WebHeroes.config as config
from WebHeroes.LobbyManagement.Errors.AlreadyOwningLobbyError import AlreadyOwningLobbyError
from WebHeroes.LobbyManagement.LobbyManager import LobbyManager
from WebHeroes.Responses import dictify, SuccessResponse, FailedResponse
from WebHeroes.Responses.ResponseTypes.LobbyRefreshResponse import LobbyRefreshResponse
from WebHeroes.Responses.DataModels.MemberModel import MemberModel
from WebHeroes.Responses.DataModels.LobbyModel import LobbyModel
from WebHeroes.UserManagement.SessionManager import SessionManager
from Leek.Repositories.UserRepository import UserRepository
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

    socket_blueprint: SocketBlueprint = SocketBlueprint(name="lobby-management")

    @staticmethod
    @socket_blueprint.on("refresh")
    def refresh() -> None:
        LobbyManagement.socket_blueprint.emit("refresh", dictify(LobbyRefreshResponse(
            members=[
                MemberModel(
                    member_id=member_id,
                    member_name=str(UserRepository.get_by_id(member_id).username)
                ) for member_id in LobbyManager.online_lobby.member_ids
            ],
            lobbies=[
                LobbyModel(
                    lobby_name=lobby.name,
                    owner_id=lobby.owner_id,
                    members=[
                        MemberModel(
                            member_id=member_id,
                            member_name=str(UserRepository.get_by_id(member_id).username)
                        ) for member_id in lobby.member_ids
                    ]
                ) for lobby in LobbyManager.get_lobbies()
            ]
        )), to=LobbyManager.online_lobby.name)

    @staticmethod
    @socket_blueprint.on("create-lobby")
    @FlaskUtil.verify_socket_arguments(socket_blueprint, lobby_name=str)
    def create_lobby(lobby_name: str) -> None:
        try:
            LobbyManager.create_lobby(lobby_name=lobby_name)
        except AlreadyOwningLobbyError as e:
            LobbyManagement.socket_blueprint.emit("create-lobby", dictify(FailedResponse(reason=str(e))))
            return

        LobbyManagement.socket_blueprint.emit("create-lobby", dictify(SuccessResponse()))
