import WebHeroes.config as config
from ZancmokLib.StaticClass import StaticClass
from flask import Blueprint


class Common(StaticClass):
    route_blueprint: Blueprint = Blueprint(
        name="WebAPI:Common",
        import_name=__name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH
    )
