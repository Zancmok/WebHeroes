from functools import wraps
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
            @wraps(function)
            def wrapper(*args, **kwargs):
                print(
                    f"Calling '{function.__name__}' "
                    f"(connection_id={connection_id}, namespace={namespace}) "
                    f"args={args}, kwargs={kwargs}",
                    flush=True
                )

                data: Any = function(*args, **kwargs)

                print("Function ended!", flush=True)

                return data

            self._connections[(connection_id, namespace)] = wrapper

            return wrapper
        return decorator

    def emit(self, event: str, *args, **kwargs) -> None:
        if self.name:
            emit(f"{self.name}:{event}", *args, **kwargs)
        else:
            emit(event, *args, **kwargs)
