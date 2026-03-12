from typing import Optional

from WebHeroes.UserManagement.UserSession import UserSession
from WebHeroes.UserManagement.SessionManager import SessionManager
from LuaBridge import LuaSandbox, BasePrototype
from Prototype import prototype_definitions, FieldType, SettingsType
from .Map import Map


class Game:
    def __init__(self, member_ids: set[int]) -> None:
        self.lua_sandbox: LuaSandbox = LuaSandbox(
            mod_paths=["core", "base"],  # "til-mod"
            prototypes=prototype_definitions
        )

        self.running: bool = False
        self.game_map: Optional[Map] = None
        self.member_ids: set[int] = member_ids
        self.users: list[UserSession] = []
        self.current_user_index: int = 0

    def run(self) -> None:
        if self.running:
            raise Exception("Game already running!")

        self.running = True

        prototypes: list[BasePrototype] = self.lua_sandbox.run()
        settings: Optional[SettingsType] = None

        fields: list[FieldType] = []
        for prototype in prototypes:
            if isinstance(prototype, SettingsType):
                settings = prototype

            if isinstance(prototype, FieldType):
                fields.append(prototype)

        self.game_map = Map(fields, settings)

        for member_id in self.member_ids:
            self.users.append(SessionManager.get_user_session_by_user_id(member_id))

    def end_turn(self) -> None:
        self.current_user_index += 1
        self.current_user_index %= len(self.users) - 1
