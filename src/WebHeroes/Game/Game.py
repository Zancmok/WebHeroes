from typing import Optional

from LuaBridge import LuaSandbox, BasePrototype
from Prototype import prototype_definitions, FieldType, SettingsType
from .Map import Map


class Game:
    def __init__(self) -> None:
        self.lua_sandbox: LuaSandbox = LuaSandbox(
            mod_paths=["core_1.0.0", "base_1.0.0"],
            prototypes=prototype_definitions
        )

        self.running: bool = False

        print("Cyka", flush=True)

        self.run()

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

        game_map: Map = Map(fields, settings)
