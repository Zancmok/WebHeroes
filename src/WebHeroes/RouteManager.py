from typing import Optional
from flask import Flask
from typing import Callable, Any


class RouteManager:
    """
    This class manages the routes for a Flask application. It allows dynamic route registration
    and stores routes in a list. The Flask application instance must be initialized using the
    `init` method before the routes can be used.
    """
    app: Optional[Flask] = None
    _routes: list[tuple[str, Callable[[Any], Any], Optional[list[str]]]] = []

    @classmethod
    def init(cls, flask_app: Flask) -> None:
        """
        Initializes the RouteManager with the provided Flask application.
        This method must be called to bind routes to the Flask app.

        :param flask_app: The Flask application instance to be managed by RouteManager.
        :return: None
        """

        if cls.app is not None:
            raise ValueError("RouteManager is already initialized with a Flask app.")

        cls.app = flask_app

        for route, endpoint, methods in cls._routes:
            cls.app.add_url_rule(route, endpoint.__name__, endpoint, methods=methods)

    @classmethod
    def route(cls, route: str, methods: Optional[list[str]] = None) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
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
            cls._routes.append((route, func, methods))
            return func

        return inner
