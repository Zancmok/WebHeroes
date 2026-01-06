from typing import Callable, Any
from flask_socketio import SocketIO


class SocketBlueprint:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self._connections: dict[tuple[str, str], Callable[..., Any]] = {}

    def init(self, socketio: SocketIO) -> None:
        for element in self._connections:
            socketio.on_event(f"{element[0]}", self._connections[element], element[1])

    def on(self, connection_id: str, namespace: str = "/") -> Callable[..., Any]:
        def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
            self._connections[(connection_id, namespace)] = function

            return function
        return decorator
