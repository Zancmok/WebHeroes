from typing import override
from WebHeroes.LobbyManagement.Lobby import Lobby


class OwnedLobby(Lobby):
    @override
    def __init__(self, name: str, owner_id: int) -> None:
        super().__init__(name)
        self.owner_id: int = owner_id

        self.join_member(owner_id)

    @override
    def __str__(self) -> str:
        return f"Lobby<name:{self.name};owner_id:{self.owner_id}>"
