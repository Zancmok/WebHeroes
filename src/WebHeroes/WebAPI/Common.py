from typing import Optional
import WebHeroes.config as config
from ZancmokLib.StaticClass import StaticClass
from ZancmokLib.SocketBlueprint import SocketBlueprint
from WebHeroes.UserManagement.SessionManager import SessionManager
from WebHeroes.LobbyManagement.Errors.AlreadyInLobbyError import AlreadyInLobbyError
from WebHeroes.LobbyManagement.LobbyManager import LobbyManager
from WebHeroes.UserManagement.Errors.SessionAlreadyBoundError import SessionAlreadyBoundError
from flask import Blueprint, request, session


class Common(StaticClass):
    route_blueprint: Blueprint = Blueprint(
        name="WebAPI:Common",
        import_name=__name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH
    )

    socket_blueprint: SocketBlueprint = SocketBlueprint(
        name="WebAPI:Common"
    )

    @staticmethod
    @socket_blueprint.on("connect")
    def on_connect(auth: Optional[dict[str, str]]) -> None:
        token: Optional[str] = str(auth.get("token")) if isinstance(auth, dict) else session.get("token")

        if not token:
            raise ConnectionRefusedError("unauthorized")
        token: str

        user_id: Optional[int]
        if not (user_id := SessionManager.get_user_id(token=token)):
            raise ConnectionRefusedError("unauthorized")
        user_id: int

        try:
            SessionManager.bind_socket_connection(socket_id=request.sid, token=token, lobby=LobbyManager.online_lobby)
        except SessionAlreadyBoundError:
            raise ConnectionRefusedError("Session already bound to another connection!")

        print(f"Client connected: {request.sid}", flush=True)

    @staticmethod
    @socket_blueprint.on("disconnect")
    def on_disconnect(reason: str) -> None:
        SessionManager.unbind_socket_connection(socket_id=request.sid)

        print(f"Client disconnected: {request.sid}", flush=True)
