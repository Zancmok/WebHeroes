from typing import Optional

from WebHeroes.UserManagement.SessionManager import SessionManager
from ZancmokLib.StaticClass import StaticClass
from WebHeroes.LobbyManagement.Lobby import Lobby
from WebHeroes.LobbyManagement.OwnedLobby import OwnedLobby
from WebHeroes.LobbyManagement.Errors.AlreadyOwningLobbyError import AlreadyOwningLobbyError
from WebHeroes.LobbyManagement.Errors.AlreadyInLobbyError import AlreadyInLobbyError


class LobbyManager(StaticClass):
    online_lobby: Lobby = Lobby(name="online-lobby")
    _player_lobbies: list[OwnedLobby] = []

    @staticmethod
    def create_lobby(lobby_name: str, token: Optional[str] = None) -> None:
        user_id: int = SessionManager.get_user_id(token=token)

        for lobby in LobbyManager._player_lobbies:
            if lobby.owner_id == user_id:
                raise AlreadyOwningLobbyError(f"User already owns lobby '{lobby.name}'")

            if user_id in lobby.member_ids:
                raise AlreadyInLobbyError(f"User already in lobby '{lobby.name}'")

        LobbyManager._player_lobbies.append(OwnedLobby(
            name=lobby_name,
            owner_id=user_id
        ))

    @staticmethod
    def get_lobbies() -> list[OwnedLobby]:
        return LobbyManager._player_lobbies
