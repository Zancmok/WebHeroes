from LuaBridge import BasePrototype


class ResourceType(BasePrototype):
    def __init__(self, name: str, display_name: str) -> None:
        super().__init__(name, display_name)
