from enum import Enum
from typing import Any

from WebHeroes.Responses.BaseDataModel import BaseDataModel
from WebHeroes.Responses.ResponseTypes.SuccessResponse import SuccessResponse
from WebHeroes.Responses.ResponseTypes.FailedResponse import FailedResponse
from WebHeroes.Responses.ResponseTypes.LoginResponse import LoginResponse
from flask import jsonify, Response


def dictify(data: BaseDataModel) -> Response:
    """
    Converts a response object into a dictionary, handling nested objects and enums.

    This function recursively converts a response object and its attributes (including nested
    objects, enums, and lists) into a dictionary representation. Enums are converted to their
    string values, and nested `BaseResponseClass` objects are recursively transformed into
    dictionaries.

    Args:
        data (BaseDataModel): The response object to convert.

    Returns:
        dict[str, Any]: The dictionary representation of the response object, where each
        attribute of the response is a key and its corresponding value is the associated value.
    """

    out: dict[str, Any] = {}

    for attribute in dir(data):
        if attribute[:2] == "__":
            continue

        attribute_value: Any = getattr(data, attribute)

        if isinstance(attribute_value, Enum):
            attribute_value = str(attribute_value.value)
        elif isinstance(attribute_value, BaseDataModel):
            attribute_value = dictify(attribute_value)
        elif isinstance(attribute_value, list):
            for i, v in enumerate(attribute_value):
                attribute_value[i] = dictify(v)

        out[attribute] = attribute_value

    return jsonify(out)


__all__ = [
    "dictify",
    "BaseDataModel",
    "SuccessResponse",
    "FailedResponse",
    "LoginResponse"
]
