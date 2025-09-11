"""
This module defines the NewUserUpdateResponse class, which represents a notification
about a new user being added. It extends from `BaseResponseClass` to follow the common
response structure.

Classes:
    NewUserUpdateResponse: A response indicating that a new user has been added to the system.
"""

from dataclasses import dataclass, field

from WebHeroes.Responses.BaseDataModel import BaseDataModel
from WebHeroes.Responses.DataModels.UserModel import UserModel


@dataclass
class NewUserUpdateModel(BaseDataModel):
    """
    Notification about a new user being added.

    This class represents a response that notifies about the addition of a new user to the system.
    It includes the user details in the `user` attribute.

    Attributes:
        object_type (str): The type of response, set to "new-user-update" to indicate that
        the response represents a new user addition.
        user (UserModel): The details of the new user, represented by a `UserResponse` object.
    """

    object_type: str = field(default="new-user-update", kw_only=True)

    user: UserModel
