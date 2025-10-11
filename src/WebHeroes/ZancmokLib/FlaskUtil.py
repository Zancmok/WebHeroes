from typing import Callable, Any

from flask import request
from ZancmokLib.StaticClass import StaticClass
from ZancmokLib.EHTTPCode import EHTTPCode
from WebHeroes.Responses import dictify
from WebHeroes.Responses.ResponseTypes.FailedResponse import FailedResponse


class FlaskUtil(StaticClass):
    @staticmethod
    def reroute_arguments(**kwargs: type) -> Callable[..., Any]:
        def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
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
                    if argument in json_data and isinstance(output_data := json_data[argument], kwargs[argument]):
                        output[argument] = output_data
                        continue

                    if argument in form_data and isinstance(output_data := form_data[argument], kwargs[argument]):
                        output[argument] = output_data
                        continue

                    if argument in query_data and isinstance(output_data := query_data[argument], kwargs[argument]):
                        output[argument] = output_data
                        continue

                    return dictify(FailedResponse(
                        reason=f"Missing or invalid argument: '{argument}'"
                    )), EHTTPCode.BAD_REQUEST

                return function(**output)
            return wrapper
        return decorator
