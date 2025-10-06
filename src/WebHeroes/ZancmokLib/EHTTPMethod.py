from enum import StrEnum, auto


class EHTTPMethod(StrEnum):
    GET = auto()
    POST = auto()
    PATCH = auto()
    PUT = auto()
    DELETE = auto()
