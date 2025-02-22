"""
dataclass_util.py

This module provides a decorator to automatically set default values for specific dataclass fields.
"""

from typing import Any
from dataclasses import dataclass, fields, is_dataclass, Field, replace, make_dataclass, field


def auto_defaults(cls: Any) -> Any:
    """
    Ensures the given class is a dataclass and automatically sets the default value
    for the 'response_type' field, making it a keyword-only argument.

    :param cls: The class to be processed (either a dataclass or a regular class).
    :return: The modified dataclass with updated defaults.
    """

    if not is_dataclass(cls):
        cls = dataclass(cls)

    class_fields: tuple[Field, ...] = fields(cls)
    new_fields: list[tuple[Any, Any, Any]] = []

    for field_obj in class_fields:
        attribute_value: Any

        if field_obj.name == "response_type":
            default_value = getattr(cls, "response_type", None)
            new_fields.append((field_obj.name, field_obj.type, field(default=default_value, kw_only=True)))
        else:
            new_fields.append((field_obj.name, field_obj.type, field(
                default=field_obj.default) if field_obj.default is not field_obj.default_factory else field(
                default_factory=field_obj.default_factory)))

    return make_dataclass(cls.__name__, new_fields, bases=(cls,))
