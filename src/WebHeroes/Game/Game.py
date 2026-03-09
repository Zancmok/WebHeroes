from typing import Optional

from LuaBridge import LuaSandbox, BasePrototype
from Prototype import prototype_definitions, FieldType, SettingsType
from .Map import Map


class Game:
    def __init__(self) -> None:
        self.lua_sandbox: LuaSandbox = LuaSandbox(
            mod_paths=["core", "base", "til-mod"],
            prototypes=prototype_definitions
        )

        self.running: bool = False
        self.game_map: Optional[Map] = None

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
