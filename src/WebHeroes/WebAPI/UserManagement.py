from typing import Optional

import WebHeroes.config as config
from WebHeroes.UserManagement.UserAccountManager import UserAccountManager
from WebHeroes.UserManagement.UserAlreadyExistsError import UserAlreadyExistsError
from Leek.Models.UserModel import UserModel
from ZancmokLib.StaticClass import StaticClass
from ZancmokLib.EHTTPMethod import EHTTPMethod
from flask import Blueprint


class UserManagement(StaticClass):
    route_blueprint: Blueprint = Blueprint(
        name="WebAPI:UserManagement",
        import_name=__name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH,
        url_prefix="/user-management"
    )

    @staticmethod
    @route_blueprint.route("/signup/", methods=[EHTTPMethod.POST])
    def signup(username: str, password: str) -> None:
        try:
            user: UserModel = UserAccountManager.create_account(username, password)
        except UserAlreadyExistsError:
            return # TODO: Do the thingy yk yk

    @staticmethod
    @route_blueprint.route("/login/", methods=[EHTTPMethod.POST])
    def login(username: str, password: str) -> None:
        user: UserModel = UserAccountManager.try_login(username, password)
