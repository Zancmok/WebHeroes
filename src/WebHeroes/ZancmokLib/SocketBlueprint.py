from typing import Callable, Any
from flask_socketio import SocketIO, emit


class SocketBlueprint:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self._connections: dict[tuple[str, str], Callable[..., Any]] = {}

    def init(self, socketio: SocketIO) -> None:
        for element in self._connections:
            if self.name:
                socketio.on_event(f"{self.name}:{element[0]}", self._connections[element], element[1])
            else:
                socketio.on_event(f"{element[0]}", self._connections[element], element[1])

    def on(self, connection_id: str, namespace: str = "/") -> Callable[..., Any]:
        def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
            self._connections[(connection_id, namespace)] = function

            return function
        return decorator

    def emit(self, event: str, *args, **kwargs) -> None:
        if self.name:
            emit(f"{self.name}:{event}", *args, **kwargs)
        else:
            emit(event, *args, **kwargs)
