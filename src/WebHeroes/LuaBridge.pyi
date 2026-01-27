from typing import Type


class BasePrototype:
    def __init__(self, name: str, display_name: str) -> None: ...

    name: str  # type: str
    display_name: str  # type: str


class PrototypeDefinition:
    def __init__(self, prototype_definition: Type[BasePrototype], synonym: str) -> None: ...

    prototype_definition: Type[BasePrototype]  # type: Type[BasePrototype]
    synonym: str  # type: str


class LuaSandbox:
    def __init__(self, prototypes: list[PrototypeDefinition], mod_paths: list[str]) -> None: ...

    prototypes: list[PrototypeDefinition]  # type: list[PrototypeDefinition]
    mod_paths: list[str]  # type: list[str]
