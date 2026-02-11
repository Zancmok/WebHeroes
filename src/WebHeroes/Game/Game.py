from LuaBridge import LuaSandbox
from Prototype import prototype_definitions


class Game:
    def __init__(self) -> None:
        self.lua_sandbox: LuaSandbox = LuaSandbox(
            mod_paths=["core", "base"],
            prototypes=prototype_definitions
        )
