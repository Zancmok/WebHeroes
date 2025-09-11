"""
Module for defining socket event names used in real-time communication.

This module contains the `SocketEvent` enum, which provides a centralized
definition of event names used in socket-based interactions.
"""

from enum import Enum


class SocketEvent(str, Enum):
    """
    Enumeration of socket event names used for real-time communication.

    Attributes:
        GET_LOBBY_DATA (str): Event for retrieving lobby data.
    """

    GET_LOBBY_DATA: str = "get-lobby-data"
    LOBBY_UPDATE: str = "lobby-update"
    CREATE_LOBBY: str = "create-lobby"
    LEAVE_LOBBY: str = "leave-lobby"
