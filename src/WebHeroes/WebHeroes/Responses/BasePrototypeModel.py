from dataclasses import dataclass


@dataclass
class BasePrototypeModel:
    object_type: str

    prototype_type: str
    name: str
