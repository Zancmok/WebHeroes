from typing import Optional

from flask import session, request
from flask_socketio import join_room, leave_room, rooms
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
        old_session: Optional[UserSession] = SessionManager.get_user_session_by_user_id(SessionManager.get_user_id(token))
        if not old_session:
            new_user_session: UserSession = UserSession(
                user_id=SessionManager.get_user_id(token),
                token=token,
                lobby=lobby
            )
            lobby.join_member(new_user_session.get_user_id())
            join_room(lobby.name)
            SessionManager._socket_connections[socket_id] = new_user_session
        else:
            old_socket_id = None
            for sid, sess in SessionManager._socket_connections.items():
                if sess is old_session:
                    old_socket_id = sid
                    break
            if old_socket_id:
                del SessionManager._socket_connections[old_socket_id]
            
            current_lobby: Lobby = old_session.get_lobby()
            join_room(current_lobby.name)
            SessionManager._socket_connections[socket_id] = old_session
            print(f"Rebound existing session for user {old_session.get_user_id()} to socket {socket_id}", flush = True)

    @staticmethod
    def unbind_socket_connection(socket_id: str) -> None:
        user_session: Optional[UserSession] = SessionManager._socket_connections.get(socket_id)
        if not user_session:
            return
        print(f"Socket {socket_id} disconnected, session preserved for user {user_session.get_user_id()}", flush=True)

    @staticmethod
    def get_user_session(socket_id: Optional[str] = None) -> Optional[UserSession]:
        if socket_id:
            return SessionManager._socket_connections.get(socket_id)

        return SessionManager._socket_connections.get(request.sid)

    @staticmethod
    def get_user_session_by_user_id(user_id: int) -> Optional[UserSession]:
        for session in SessionManager._socket_connections.values():
            if session.get_user_id() == user_id:
                return session
        return None
