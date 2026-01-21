class BasePrototype:
    def __init__(self, type: str, name: str) -> None: ...

    type: str  # type: str
    name: str  # type: str


class LuaSandbox:
    def __init__(self, prototypes: list[BasePrototype], mods: list[str]) -> None: ...

    prototypes: list[BasePrototype]  # type: list[BasePrototype]
    mods: list[str]  # type: list[str]
