from typing import Optional
import WebHeroes.config as config
from ZancmokLib.StaticClass import StaticClass
from ZancmokLib.SocketBlueprint import SocketBlueprint
from WebHeroes.UserManagement.SessionManager import SessionManager
from WebHeroes.LobbyManagement.Errors.AlreadyInLobbyError import AlreadyInLobbyError
from WebHeroes.LobbyManagement.LobbyManager import LobbyManager
from flask import Blueprint


class Common(StaticClass):
    route_blueprint: Blueprint = Blueprint(
        name="WebAPI:Common",
        import_name=__name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH
    )

    socket_blueprint: SocketBlueprint = SocketBlueprint(
        name=""
    )

    @staticmethod
    @socket_blueprint.on("connect")
    def on_connect(auth: Optional[dict[str, str]]) -> None:
        user_id: int
        if not (user_id := SessionManager.get_user_id((auth.get("token") if isinstance(auth, dict) else None))):
            raise ConnectionRefusedError("unauthorized")

        try:
            LobbyManager.online_lobby.join_member(user_id)
        except AlreadyInLobbyError:
            raise ConnectionRefusedError("User already connected!")

        print(f"Client connected!", flush=True)

    @staticmethod
    @socket_blueprint.on("disconnect")
    def on_disconnect(reason: str) -> None:
        user_id: Optional[int] = SessionManager.get_user_id()

        if user_id:
            LobbyManager.online_lobby.leave_member(user_id)

        print(f"Client disconnected: {reason}", flush=True)
