from types import NoneType
from typing import Optional

import WebHeroes.config as config
from WebHeroes.UserManagement.Errors.AlreadyLoggedInError import AlreadyLoggedInError
from WebHeroes.UserManagement.Errors.AuthFailedError import AuthFailedError
from WebHeroes.UserManagement.UserAccountManager import UserAccountManager
from WebHeroes.UserManagement.Errors.UserAlreadyExistsError import UserAlreadyExistsError
from WebHeroes.UserManagement.Errors.InvalidUsernameError import InvalidUsernameError
from WebHeroes.UserManagement.Errors.UserDoesntExistError import UserDoesntExistError
from WebHeroes.Errors.NotLoggedInError import NotLoggedInError
from ZancmokLib.StaticClass import StaticClass
from ZancmokLib.EHTTPMethod import EHTTPMethod
from ZancmokLib.EHTTPCode import EHTTPCode, HTTPCode
from ZancmokLib.FlaskUtil import FlaskUtil
from flask import Blueprint, Response
from WebHeroes.Responses.ResponseTypes.SuccessResponse import SuccessResponse
from WebHeroes.Responses.ResponseTypes.FailedResponse import FailedResponse
from WebHeroes.Responses.ResponseTypes.LoginResponse import LoginResponse
from WebHeroes.Responses import jsonify


class UserManagement(StaticClass):
    route_blueprint: Blueprint = Blueprint(
        name="WebAPI:UserManagement",
        import_name=__name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH,
        url_prefix="/user-management"
    )

    @staticmethod
    @route_blueprint.route("/signup", methods=[EHTTPMethod.POST])
    @FlaskUtil.reroute_arguments(username=str, password=str)
    def signup(username: str, password: str) -> tuple[Response, HTTPCode]:
        try:
            UserAccountManager.create_account(
                username=username,
                password=password
            )
        except InvalidUsernameError as e:
            return jsonify(FailedResponse(
                reason=str(e)
            )), EHTTPCode.BAD_REQUEST
        except UserAlreadyExistsError as e:
            return jsonify(FailedResponse(
                reason=str(e)
            )), EHTTPCode.CONFLICT
        
        return jsonify(SuccessResponse()), EHTTPCode.CREATED

    @staticmethod
    @route_blueprint.route("/login", methods=[EHTTPMethod.POST])
    @FlaskUtil.reroute_arguments(username=str, password=str)
    def login(username: str, password: str) -> tuple[Response, HTTPCode]:
        try:
            token: str = UserAccountManager.try_login(username, password)
        except UserDoesntExistError as e:
            return jsonify(FailedResponse(
                reason=str(e)
            )), EHTTPCode.BAD_REQUEST
        except AuthFailedError as e:
            return jsonify(FailedResponse(
                reason=str(e)
            )), EHTTPCode.BAD_REQUEST
        except AlreadyLoggedInError as e:
            return jsonify(FailedResponse(
                reason=str(e)
            )), EHTTPCode.FORBIDDEN

        return jsonify(LoginResponse(
            token=token
        )), EHTTPCode.OK

    @staticmethod
    @route_blueprint.route("/logout", methods=[EHTTPMethod.POST])
    @FlaskUtil.reroute_arguments(token=[str, NoneType])
    def logout(token: Optional[str] = None) -> tuple[Response, HTTPCode]:
        try:
            UserAccountManager.try_logout(token=token)
        except NotLoggedInError:
            return jsonify(FailedResponse(
                reason="Cannot log out if not logged in."
            )), EHTTPCode.FORBIDDEN

        return jsonify(SuccessResponse()), EHTTPCode.OK
