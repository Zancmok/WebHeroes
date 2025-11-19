import WebHeroes.config as config
from ZancmokLib.StaticClass import StaticClass
from ZancmokLib.SocketBlueprint import SocketBlueprint
from flask import Blueprint


class Common(StaticClass):
    route_blueprint: Blueprint = Blueprint(
        name="WebAPI:Common",
        import_name=__name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH
    )

    socket_blueprint: SocketBlueprint = SocketBlueprint(
        name=""
    )

    @staticmethod
    @socket_blueprint.on("connect")
    def on_connect() -> None:
        print("Client connected (:", flush=True)

    @staticmethod
    @socket_blueprint.on("disconnect")
    def on_disconnect() -> None:
        print("Client disconnected ):", flush=True)
