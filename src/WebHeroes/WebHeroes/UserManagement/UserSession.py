from WebHeroes.LobbyManagement.Lobby import Lobby


class UserSession:
    def __init__(self, user_id: int, token: str, lobby: Lobby) -> None:
        self._user_id = user_id
        self._token: str = token
        self._lobby: Lobby = lobby

    def __str__(self) -> str:
        return f"UserSession(user_id={self._user_id}, token={self._token}, lobby={self._lobby.__str__()})"

    def get_user_id(self) -> int:
        return self._user_id
    
    def get_token(self) -> str:
        return self._token
    
    def get_lobby(self) -> Lobby:
        return self._lobby

    def join_lobby(self, lobby: Lobby) -> None:
        if lobby is self._lobby:
            return

        self._lobby.leave_member(self._user_id)

        self._lobby = lobby

        lobby.join_member(self._user_id)
        