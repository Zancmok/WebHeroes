"""
This module defines the UserUpdatedUpdateResponse class, which represents a notification
about a user's information being updated. It extends from `BaseResponseClass` to follow
the common response structure.

Classes:
    UserUpdatedUpdateResponse: A response indicating that a user's information has been
    updated.
"""

from dataclasses import dataclass, field

from WebHeroes.Responses.BaseDataModel import BaseDataModel


@dataclass
class UserUpdatedUpdateModel(BaseDataModel):
    """
    Notification about a user's information being updated.

    This class represents a response indicating that a user's information has been updated
    in the system. It contains a specific `object_type` to distinguish this as a "user-updated-update"
    response.

    Attributes:
        object_type (str): The type of response, set to "user-updated-update" to indicate
        that the response represents an update to a user's information.
    """

    object_type: str = field(default="user-updated-update", kw_only=True)
