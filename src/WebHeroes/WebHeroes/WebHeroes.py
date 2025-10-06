"""
WebHeroes.py

This module defines the `WebHeroes` class, which serves as the main interface for managing the web server,
handling authentication, and providing various routes for the Flask application.

Classes:
    WebHeroes: A static class that configures and manages the Flask web application and its integration
    with the Discord API.
"""

from flask import Flask
from flask_socketio import SocketIO
from Leek.Leek import Leek
import WebHeroes.config as config
from ZancmokLib.StaticClass import StaticClass
from WebAPI.Common import Common
from WebAPI.HTMLRoutes import HTMLRoutes
from WebAPI.UserManagement import UserManagement


class WebHeroes(StaticClass):
    """
    The main class that serves as the primary interface between the server and clients.
    It handles the initialization of the Flask application, manages authentication with Discord,
    and provides necessary setup for the web application to function correctly. This class
    also manages the routes for various web pages and features.

    This class should be used to configure and run the web server, initialize the required
    services (like the Discord API client), and serve dynamic content via Flask routes.

    Attributes:
        app: A Flask instance that handles the web server and routing.

    Methods:
        run: Initializes and starts the Flask web server.
    """

    app: Flask = Flask(
        __name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH
    )

    socket_io: SocketIO = SocketIO(app)

    @staticmethod
    def run() -> None:
        """
        Initializes the Flask application and starts the web server. This method must be
        called to start the web application. It also sets up necessary configurations,
        including the session secret key.

        :return: None
        """

        WebHeroes.app.register_blueprint(Common.route_blueprint)
        WebHeroes.app.register_blueprint(HTMLRoutes.route_blueprint)
        WebHeroes.app.register_blueprint(UserManagement.route_blueprint)

        Leek.initialize()

        WebHeroes.app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY

        WebHeroes.socket_io.run(
            WebHeroes.app,
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            use_reloader=False,
            log_output=True
        )
