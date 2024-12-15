class StaticClass:
    """
    A base class that prevents the creation of instances.

    This class is designed to be used as a base class for static classes, where
    the intention is to prevent instantiation. When an attempt is made to instantiate
    a class that inherits from `StaticClass`, a `TypeError` is raised.
    """

    def __new__(cls, *args, **kwargs) -> None:
        raise TypeError(f"Cannot create: '{cls.__name__}', the class is static!")
