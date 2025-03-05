"""
# TODO: Write Docstring!
"""

from typing import Any
from enum import Enum
from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.ResponseTypes.EmptyResponse import EmptyResponse
from WebHeroes.ResponseTypes.UserResponse import UserResponse
from WebHeroes.ResponseTypes.LobbyResponse import LobbyResponse
from WebHeroes.ResponseTypes.GetLobbyDataResponse import GetLobbyDataResponse
from WebHeroes.ResponseTypes.NewUserUpdateResponse import NewUserUpdateResponse
from WebHeroes.ResponseTypes.NewLobbyUpdateResponse import NewLobbyUpdateResponse
from WebHeroes.ResponseTypes.UserUpdatedUpdateResponse import UserUpdatedUpdateResponse
from WebHeroes.ResponseTypes.LobbyUpdateResponse import LobbyUpdateResponse
from WebHeroes.ResponseTypes.UserLeftUpdateResponse import UserLeftUpdateResponse


def dictify(data: BaseResponseClass) -> dict[str, Any]:
    """
    Converts a response object into a dictionary, handling nested objects and enums.

    Args:
        data (BaseResponseClass): The response object to convert.

    Returns:
        dict[str, Any]: The dictionary representation of the response object.
    """

    out: dict[str, Any] = {}

    for attribute in dir(data):
        if attribute[:2] == "__":
            continue

        attribute_value: Any = getattr(data, attribute)

        if isinstance(attribute_value, Enum):
            attribute_value = str(attribute_value.value)
        elif isinstance(attribute_value, BaseResponseClass):
            attribute_value = dictify(attribute_value)
        elif isinstance(attribute_value, list):
            for i, v in enumerate(attribute_value):
                attribute_value[i] = dictify(v)

        out[attribute] = attribute_value

    return out


__all__ = [
    "dictify",
    "BaseResponseClass",
    "EmptyResponse",
    "UserResponse",
    "LobbyResponse",
    "GetLobbyDataResponse",
    "NewUserUpdateResponse",
    "NewLobbyUpdateResponse",
    "UserUpdatedUpdateResponse",
    "LobbyUpdateResponse",
    "UserLeftUpdateResponse"
]
