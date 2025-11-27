from typing import Optional

from flask import session
from flask_socketio import join_room, leave_room
from WebHeroes.LobbyManagement.Lobby import Lobby
from WebHeroes.UserManagement.Errors.SessionAlreadyBoundError import SessionAlreadyBoundError
from WebHeroes.UserManagement.UserSession import UserSession
from ZancmokLib.StaticClass import StaticClass
import secrets


class SessionManager(StaticClass):
    _tokens: dict[str, int] = {}
    _socket_connections: dict[str, UserSession] = {}

    @staticmethod
    def new_session(user_id: int) -> str:
        token: str = secrets.token_urlsafe(32)

        SessionManager._tokens[token] = user_id
        session["token"] = token

        return token

    @staticmethod
    def get_user_id(token: Optional[str] = None) -> Optional[int]:
        if token:
            return SessionManager._tokens.get(token)

        return SessionManager._tokens.get(session.get("token"))

    @staticmethod
    def kill_session(token: Optional[str] = None) -> None:
        if not token:
            token = session.get("token")
        token: str

        if session.get("token"):
            session.pop("token")

        SessionManager._tokens.pop(token, None)

    @staticmethod
    def get_session(user_id: int) -> Optional[str]:
        for token in SessionManager._tokens:
            if SessionManager._tokens[token] == user_id:
                return token

        return None

    @staticmethod
    def refresh_session(token: str) -> None:
        if not session.get("token"):
            session["token"] = token

    @staticmethod
    def bind_socket_connection(socket_id: str, token: str, lobby: Lobby) -> None:
        for user_session in SessionManager._socket_connections.values():
            if user_session.get_token() == token:
                raise SessionAlreadyBoundError

        new_user_session: UserSession = UserSession(
            user_id=SessionManager.get_user_id(token),
            token=token,
            lobby=lobby
        )

        lobby.join_member(new_user_session.get_user_id())
        join_room(lobby.name)

        SessionManager._socket_connections[socket_id] = new_user_session

    @staticmethod
    def unbind_socket_connection(socket_id: str) -> None:
        user_session: UserSession = SessionManager._socket_connections.pop(socket_id)

        lobby: Lobby = user_session.get_lobby()

        lobby.leave_member(user_session.get_user_id())
        leave_room(lobby.name)
