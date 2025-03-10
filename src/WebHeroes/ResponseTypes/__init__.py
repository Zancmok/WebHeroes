"""
This module contains a utility function `dictify` that converts response objects
into dictionary representations, handling nested objects and enumerations.

It also imports various response classes used within the system, making them available
for use in the module. These classes represent different types of responses in the system,
such as lobby updates and user data.

Functions:
    dictify (BaseResponseClass) -> dict[str, Any]: Converts a response object into
    a dictionary, handling nested objects, enums, and lists.

Imports:
    BaseResponseClass: The base class for all response types.
    EmptyResponse: Represents an empty response.
    UserResponse: Represents a user-related response.
    LobbyResponse: Represents a lobby-related response.
    GetLobbyDataResponse: Represents a response for getting lobby data.
    NewUserUpdateResponse: Represents a response for a new user update.
    NewLobbyUpdateResponse: Represents a response for a new lobby update.
    UserUpdatedUpdateResponse: Represents a response for an updated user.
    LobbyUpdateResponse: Represents a response for a lobby update.
    UserLeftUpdateResponse: Represents a response for a user leaving.
"""

from enum import Enum
from typing import Any

from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.ResponseTypes.EmptyResponse import EmptyResponse
from WebHeroes.ResponseTypes.GetLobbyDataResponse import GetLobbyDataResponse
from WebHeroes.ResponseTypes.LobbyResponse import LobbyResponse
from WebHeroes.ResponseTypes.LobbyUpdateResponse import LobbyUpdateResponse
from WebHeroes.ResponseTypes.NewLobbyUpdateResponse import NewLobbyUpdateResponse
from WebHeroes.ResponseTypes.NewUserUpdateResponse import NewUserUpdateResponse
from WebHeroes.ResponseTypes.UserLeftUpdateResponse import UserLeftUpdateResponse
from WebHeroes.ResponseTypes.UserResponse import UserResponse
from WebHeroes.ResponseTypes.UserUpdatedUpdateResponse import UserUpdatedUpdateResponse
from WebHeroes.ResponseTypes.SuccessResponse import SuccessResponse


def dictify(data: BaseResponseClass) -> dict[str, Any]:
    """
    Converts a response object into a dictionary, handling nested objects and enums.

    This function recursively converts a response object and its attributes (including nested
    objects, enums, and lists) into a dictionary representation. Enums are converted to their
    string values, and nested `BaseResponseClass` objects are recursively transformed into
    dictionaries.

    Args:
        data (BaseResponseClass): The response object to convert.

    Returns:
        dict[str, Any]: The dictionary representation of the response object, where each
        attribute of the response is a key and its corresponding value is the associated value.
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
    "UserLeftUpdateResponse",
    "SuccessResponse"
]
