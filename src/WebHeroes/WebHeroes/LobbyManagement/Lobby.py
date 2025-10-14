class Lobby:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.member_ids: list[int] = []

    def join_member(self, member_id: int) -> None:
        self.member_ids.append(member_id)

    def leave_member(self, member_id: int) -> None:
        self.member_ids.remove(member_id)

    def __str__(self) -> str:
        return f"Lobby<name:{self.name}>"
