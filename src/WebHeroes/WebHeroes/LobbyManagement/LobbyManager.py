from ZancmokLib.StaticClass import StaticClass
from WebHeroes.LobbyManagement.Lobby import Lobby
from WebHeroes.LobbyManagement.OwnedLobby import OwnedLobby


class LobbyManager(StaticClass):
    online_lobby: Lobby = Lobby(name="online-lobby")
    player_lobbies: list[OwnedLobby] = []
