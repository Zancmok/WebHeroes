from typing import Optional

from flask import session

from ZancmokLib.StaticClass import StaticClass
import secrets


class SessionManager(StaticClass):
    _tokens: dict[str, int] = {}

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
