from LuaBridge import LuaSandbox
from Prototype import prototype_definitions, FieldType


class Game:
    def __init__(self) -> None:
        self.lua_sandbox: LuaSandbox = LuaSandbox(
            mod_paths=["core_1.0.0", "base_1.0.0"],
            prototypes=prototype_definitions
        )

        self.lua_sandbox.run()
