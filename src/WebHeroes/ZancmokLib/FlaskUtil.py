from typing import Callable, Any

import functools
from flask import request, redirect
from ZancmokLib.StaticClass import StaticClass
from ZancmokLib.EHTTPCode import EHTTPCode
from WebHeroes.UserManagement.SessionManager import SessionManager
from WebHeroes.Responses import dictify
from WebHeroes.Responses.ResponseTypes.FailedResponse import FailedResponse
from WebHeroes.UserManagement.EUserPermissionLevel import EUserPermissionLevel
from Leek.Repositories.UserRepository import UserRepository
from Leek.Models.UserModel import UserModel


class FlaskUtil(StaticClass):
    @staticmethod
    def reroute_arguments(**kwargs: type | list[type]) -> Callable[..., Any]:
        def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(function)
            def wrapper() -> Any:
                if not isinstance(json_data := request.get_json(silent=True), dict):
                    json_data = {}
                json_data: dict[str, Any]

                if not isinstance(form_data := request.form.to_dict(), dict):
                    form_data = {}
                form_data: dict[str, Any]

                if not isinstance(query_data := request.args.to_dict(), dict):
                    query_data = {}
                query_data: dict[str, Any]

                output: dict[str, Any] = {}
                for argument in kwargs:
                    allowed_types: tuple[type]
                    if isinstance(kwargs[argument], type):
                        allowed_types = (kwargs[argument],)
                    else:
                        allowed_types = tuple(kwargs[argument])

                    if argument in json_data and isinstance(output_data := json_data[argument], allowed_types):
                        output[argument] = output_data
                        continue

                    if argument in form_data and isinstance(output_data := form_data[argument], allowed_types):
                        output[argument] = output_data
                        continue

                    if argument in query_data and isinstance(output_data := query_data[argument], allowed_types):
                        output[argument] = output_data
                        continue

                    return dictify(FailedResponse(
                        reason=f"Missing or invalid argument: '{argument}'"
                    )), EHTTPCode.BAD_REQUEST

                return function(**output)
            return wrapper
        return decorator

    @staticmethod
    def require_auth(permission_level: EUserPermissionLevel = EUserPermissionLevel.DEFAULT) -> Callable[..., Any]:
        def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(function)
            def wrapper(*args, **kwargs) -> Any:
                if not (user_id := SessionManager.get_user_id(kwargs.get("token"))):
                    return redirect(
                        "/signup/",
                        code=EHTTPCode.FOUND)
                user_id: int

                if not (user := UserRepository.get_by_id(user_id)):
                    return dictify(FailedResponse(
                        reason="User not found."
                    )), EHTTPCode.FORBIDDEN
                user: UserModel

                if user.permission_level.value < permission_level.value:
                    return dictify(FailedResponse(
                        reason="Insufficient permissions."
                    )), EHTTPCode.FORBIDDEN

                return function(*args, **kwargs)
            return wrapper
        return decorator
