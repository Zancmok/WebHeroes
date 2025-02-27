"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field
from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass


@dataclass
class NewUserUpdateResponse(BaseResponseClass):
    """
    Notification about a new user joining the system.
    """

    object_type: str = field(default="new-user-update", kw_only=True)
