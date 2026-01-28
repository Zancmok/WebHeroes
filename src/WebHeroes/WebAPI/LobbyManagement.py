from typing import Any
import WebHeroes.config as config
from WebHeroes.LobbyManagement.Errors.AlreadyInLobbyError import AlreadyInLobbyError
from WebHeroes.LobbyManagement.Errors.AlreadyOwningLobbyError import AlreadyOwningLobbyError
from WebHeroes.LobbyManagement.Lobby import Lobby
from WebHeroes.LobbyManagement.LobbyManager import LobbyManager
from WebHeroes.LobbyManagement.OwnedLobby import OwnedLobby
from WebHeroes.Responses import dictify, SuccessResponse, FailedResponse
from WebHeroes.Responses.ResponseTypes.LobbyRefreshResponse import LobbyRefreshResponse
from WebHeroes.Responses.ResponseTypes.GetLobbyResponse import GetLobbyResponse
from WebHeroes.Responses.DataModels.MemberModel import MemberModel
from WebHeroes.Responses.DataModels.LobbyModel import LobbyModel
from WebHeroes.UserManagement.SessionManager import SessionManager
from Leek.Repositories.UserRepository import UserRepository
from flask import Blueprint, Response

from WebHeroes.UserManagement.UserSession import UserSession
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
    @socket_blueprint.on("get-lobby")
    def get_lobby() -> None:
        if not (user_session := SessionManager.get_user_session()):
            return
        user_session: UserSession

        lobby: Lobby = user_session.get_lobby()
        if not isinstance(lobby, OwnedLobby):
            return
        lobby: OwnedLobby

        LobbyManagement.socket_blueprint.emit("get-lobby", dictify(GetLobbyResponse(
            owner=MemberModel(
                member_id=lobby.owner_id,
                member_name=str(UserRepository.get_by_id(lobby.owner_id).username)
            ),
            members=[
                MemberModel(
                    member_id=member_id,
                    member_name=str(UserRepository.get_by_id(member_id).username)
                ) for member_id in lobby.member_ids
            ]
        )), to=lobby.name)

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

    @staticmethod
    @socket_blueprint.on("join-lobby")
    @FlaskUtil.verify_socket_arguments(socket_blueprint, lobby_name=str)
    def join_lobby(lobby_name: str) -> None:
        if not (user_session := SessionManager.get_user_session()):
            return
        user_session: UserSession

        lobbies: list[OwnedLobby] = LobbyManager.get_lobbies()
        for lobby in lobbies:
            if lobby.name == lobby_name:
                try:
                    user_session.join_lobby(lobby)
                except AlreadyInLobbyError as e:
                    LobbyManagement.socket_blueprint.emit("join-lobby", dictify(FailedResponse(reason=str(e))))
                    return

                break
