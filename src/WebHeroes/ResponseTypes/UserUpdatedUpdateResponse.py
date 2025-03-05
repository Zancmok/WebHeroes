"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field

from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass


@dataclass
class UserUpdatedUpdateResponse(BaseResponseClass):
    """
    Notification about a user's information being updated.
    """

    object_type: str = field(default="user-updated-update", kw_only=True)
