from WebHeroes.LobbyManagement.Errors.AlreadyInLobbyError import AlreadyInLobbyError


class Lobby:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.member_ids: set[int] = set()

    def join_member(self, member_id: int) -> None:
        if member_id in self.member_ids:
            raise AlreadyInLobbyError

        self.member_ids.add(member_id)

    def leave_member(self, member_id: int) -> None:
        self.member_ids.remove(member_id)

    def __str__(self) -> str:
        return f"Lobby(name={self.name})"
