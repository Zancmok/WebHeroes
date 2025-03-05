"""
# TODO: Write Docstring!
"""

from dataclasses import dataclass, field

from WebHeroes.ResponseTypes.BaseResponseClass import BaseResponseClass


@dataclass
class NewLobbyUpdateResponse(BaseResponseClass):
    """
    Notification about a new lobby being created.
    """

    object_type: str = field(default="new-lobby-update", kw_only=True)
