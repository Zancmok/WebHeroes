from WebHeroes.LobbyManagement.OwnedLobby import OwnedLobby
from LuaBridge import LuaSandbox
from Prototype import prototype_definitions


class Game:
    def __init__(self, lobby: OwnedLobby) -> None:
        self.lobby: OwnedLobby = lobby
        self.lua_sandbox: LuaSandbox = LuaSandbox(
            mod_paths=["core", "base"],
            prototypes=prototype_definitions
        )
