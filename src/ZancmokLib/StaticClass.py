"""
StaticClass.py

This module defines the `StaticClass` class, a base class that prevents the
instantiation of any subclass. It is designed to enforce the pattern of static
classes, where creating instances of the class doesn't make sense, and only
static methods or constants are intended to be used.

The primary purpose of `StaticClass` is to act as a base class for classes that
are meant to only contain static methods or constants, ensuring that no instance
of the class can be created. Any attempt to instantiate a class that inherits from
`StaticClass` will raise a `TypeError`.

Classes:
    StaticClass: A base class that prevents instantiation of any class that
                 inherits from it, ensuring that the class is used purely for
                 static methods or constants.

Usage:

    To use `StaticClass`, create a subclass that contains only static methods or
    constants. Any attempt to instantiate the subclass will raise a `TypeError`.

    Example:
        class MathHelper(StaticClass):
            @staticmethod
            def add(a, b):
                return a + b

        # This will raise a TypeError
        try:
            obj = MathHelper()
        except TypeError as e:
            print(e)  # Output: "Cannot create: 'MathHelper', the class is static!"

        # Static methods can still be accessed directly
        result = MathHelper.add(3, 4)  # Returns 7
"""


class StaticClass:
    """
    A base class that prevents the creation of instances.

    This class is designed to be used as a base class for static classes, where
    the intention is to prevent instantiation. When an attempt is made to instantiate
    a class that inherits from `StaticClass`, a `TypeError` is raised.
    """

    def __new__(cls, *args, **kwargs) -> None:
        raise TypeError(f"Cannot create: '{cls.__name__}', the class is static!")
