"""
RouteManager.py

This module defines the `RouteManager` class, which facilitates dynamic route
registration for a Flask application. The class provides mechanisms for storing route
definitions and registering them with a Flask app when needed.

Classes:
    RouteManager: Manages Flask application routes, enabling dynamic route registration
                  and providing a decorator for route handler functions.

Usage:
    route_manager = RouteManager()

    @route_manager.route("/example", methods=["GET"])
    def example_handler():
        return "Example route"

    app = Flask(__name__)
    route_manager.register_routes(app)
"""

from typing import Optional, Callable, Any
from flask import Flask


class RouteManager:
    """
    Manages routes for a Flask application. This class allows dynamic route
    registration and provides a decorator for registering route handler functions.

    Attributes:
        flask_app (Optional[Flask]): The Flask application instance associated
                                      with this route manager. It is set once
                                      `register_routes` is called.
        _routes (list[tuple[str, Callable[[Any], Any], Optional[list[str]]]]):
                A list of routes and their associated handler functions and HTTP
                methods. This list stores the route definitions before they are
                registered with the Flask app.
    """

    def __init__(self) -> None:
        self.flask_app: Optional[Flask] = None
        self._routes: list[tuple[str, Callable[[Any], Any], Optional[list[str]]]] = []

    def register_routes(self, flask_app: Flask) -> None:
        """
        Registers all routes stored in the RouteManager with the provided Flask app.

        This method sets the `flask_app` attribute to the provided Flask app and
        adds all routes from the `_routes` list to the app. Each route is registered
        with the corresponding HTTP methods.

        :param flask_app: The Flask application instance to register the routes with.
        :return: None
        :raises ValueError: If the RouteManager has already been initialized with a Flask app.
        """

        if self.flask_app is not None:
            raise ValueError("RouteManager is already initialized with a Flask app.")

        self.flask_app = flask_app

        for route, endpoint, methods in self._routes:
            self.flask_app.add_url_rule(route, endpoint.__name__, endpoint, methods=methods)

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
