"""
RouteManager.py

This module defines the `RouteManager` class, which facilitates dynamic registration
of both HTTP routes and WebSocket events in a Flask application. It allows for
flexible routing and event handling by storing route definitions and registering
them with a Flask app when needed.

Classes:
    RouteManager: Manages Flask application routes and WebSocket events,
                  providing decorators for dynamic registration.

Usage:
    route_manager = RouteManager()

    @route_manager.route("/example", methods=["GET"])
    def example_handler():
        return "Example route"

    @route_manager.event("message")
    def handle_message(data):
        print("Received:", data)

    app = Flask(__name__)
    socketio = SocketIO(app)
    route_manager.register_routes(app, socketio)
"""

from typing import Optional, Callable, Any

from flask import Flask
from flask_socketio import SocketIO


class RouteManager:
    """
    Manages HTTP routes and WebSocket events for a Flask application.

    This class provides decorators for dynamically registering Flask routes and
    Socket.IO event handlers. Routes and events are stored until explicitly registered
    with a Flask application and a Socket.IO instance.

    Attributes:
        flask_app (Optional[Flask]): The Flask application instance associated
                                     with this route manager. Set when `register_routes` is called.
        flask_socket_io (Optional[SocketIO]): The Socket.IO instance associated with
                                              this route manager, enabling WebSocket event handling. Set when `register_routes` is called.
        _routes (list[tuple[str, Callable[[Any], Any], Optional[list[str]]]]):
            A list of HTTP routes with their associated handler functions and HTTP methods.
        _events (list[tuple[str, Callable[[Any], Any], Optional[str]]]):
            A list of WebSocket event names, their handlers, and optional namespaces.
    """

    def __init__(self) -> None:
        self.flask_app: Optional[Flask] = None
        self.flask_socket_io: Optional[SocketIO] = None
        self._routes: list[tuple[str, Callable[[Any], Any], Optional[list[str]]]] = []
        self._events: list[tuple[str, Callable[[Any], Any], Optional[str]]] = []

    def register_routes(self, flask_app: Flask, flask_socket_io: SocketIO) -> None:
        """
        Registers all stored HTTP routes and WebSocket events with the provided Flask app and Socket.IO instance.

        This method binds all registered routes to the Flask app and all WebSocket events
        to the Socket.IO instance. It prevents re-registration if already initialized.

        :param flask_app: The Flask application instance to register routes with.
        :param flask_socket_io: The Socket.IO instance to register WebSocket events with.
        :raises ValueError: If the RouteManager is already initialized with a Flask app.
        """

        if self.flask_app is not None:
            raise ValueError("RouteManager is already initialized with a Flask app.")

        self.flask_app = flask_app
        self.flask_socket_io = flask_socket_io

        for route, endpoint, methods in self._routes:
            self.flask_app.add_url_rule(route, endpoint.__name__, endpoint, methods=methods)

        for name, handler, namespace in self._events:
            self.flask_socket_io.on_event(name, handler, namespace)

    def route(self, route: str, methods: Optional[list[str]] = None) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """
        Registers a new route for the Flask app managed by RouteManager.
        The decorated function will be added to the list of routes and registered
        with the Flask app once `init` is called.

        :param route: The URL route that the function should be registered to.
        :param methods: A list of HTTP methods (e.g., ['GET', 'POST']) this route should handle.
                        Defaults to ['GET'] if not provided.
        :return: A decorator that registers the function as a route handler.
        """

        if methods is None:
            methods = ['GET']  # Default method is GET

        def inner(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            """
            The inner decorator that actually registers the function to the route.

            :param func: The function to be registered as a route handler.
            :return: The same function that is decorated with the route.
            """
            self._routes.append((route, func, methods))
            return func

        return inner

    def event(self, name: str, namespace: Optional[str] = None) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """
        Decorator for registering a WebSocket event with the Flask-SocketIO instance.

        The decorated function will be stored and later registered as an event
        handler when `register_routes` is called.

        :param name: The WebSocket event name.
        :param namespace: (Optional) The namespace to associate with the event.
        :return: A decorator that registers the function as an event handler.
        """
        def inner(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            """
            Inner decorator function that stores the WebSocket event definition.

            :param func: The function to be registered as an event handler.
            :return: The original function, unmodified.
            """

            self._events.append((name, func, namespace))
            return func

        return inner
