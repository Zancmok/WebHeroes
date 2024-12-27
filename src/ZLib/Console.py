from ZLib.StaticClass import StaticClass
from typing import Optional


class Console(StaticClass):
    """
    A utility class for enhanced console output. This class provides static methods
    for printing messages with specific formatting, such as standard messages and warnings.
    Inherits from `StaticClass`.
    """

    @staticmethod
    def print(*args, sep: Optional[str] = "", end: Optional[str] = "\n") -> None:
        """
        Prints a message to the console with a `> ` prefix for standard output formatting.

        Args:
            *args: The message components to be printed. These will be concatenated with `sep`.
            sep (Optional[str]): The separator string between message components. Defaults to an empty string.
            end (Optional[str]): The string appended at the end of the message. Defaults to a newline character.

        Returns:
            None
        """

        return print(
            "> ",
            *args,
            sep=sep,
            end=end
        )

    @staticmethod
    def warn(*args, sep: Optional[str] = "", end: Optional[str] = "\n") -> None:
        """
        Prints a warning message to the console with a `WARNING: ` prefix.

        Args:
            *args: The warning message components to be printed. These will be concatenated with `sep`.
            sep (Optional[str]): The separator string between message components. Defaults to an empty string.
            end (Optional[str]): The string appended at the end of the message. Defaults to a newline character.

        Returns:
            None
        """

        return print(
            "WARNING: ",
            *args,
            sep=sep,
            end=end
        )
