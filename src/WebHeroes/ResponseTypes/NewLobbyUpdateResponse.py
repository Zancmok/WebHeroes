"""
This module defines the NewLobbyUpdateResponse class, which represents a notification
about a new lobby being created. It extends from `BaseResponseClass` to ensure consistent
structure across response objects.

Classes:
    NewLobbyUpdateResponse: A response indicating that a new lobby has been created.
"""

from dataclasses import dataclass, field

from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass
from WebHeroes.ResponseTypes.UserResponse import UserResponse


@dataclass
class NewLobbyUpdateResponse(BaseResponseClass):
    """
    Notification about a new lobby being created.

    This class is used to represent a response that notifies about the creation of a new lobby.
    It includes a specific `object_type` to distinguish it as a "new-lobby-update" type response.

    Attributes:
        object_type (str): The type of response, set to "new-lobby-update" to indicate that
        the response represents a new lobby creation.
    """

    object_type: str = field(default="new-lobby-update", kw_only=True)

    # TODO: Update Docstring!

    lobby_name: str
    owner: UserResponse
