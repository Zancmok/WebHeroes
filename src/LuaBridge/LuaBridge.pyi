from typing import Type


class BasePrototype:
    def __init__(self, type: str, name: str) -> None: ...

    type: str  # type: str
    name: str  # type: str


class LuaSandbox:
    def __init__(self, prototypes: list[Type[BasePrototype]], mod_paths: list[str]) -> None: ...

    prototypes: list[Type[BasePrototype]]  # type: list[Type[BasePrototype]]
    mod_paths: list[str]  # type: list[str]
