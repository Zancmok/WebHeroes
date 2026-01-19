"""
main.py

This module defines the entry point for running the main logic of the program.
It checks for the existence of a `.env` file and ensures that the program should
only run if certain conditions are met. If the conditions are not met, the program
will notify the user and exit early.

The `main()` function orchestrates the setup and execution of the program, and it
only runs the core functionality if the environment is correctly configured.
"""

import os


def main() -> None:
    """
    Runs the main class.
    :return:
    """

    import LuaBridge

    print(dir(LuaBridge))

    return

    if not os.path.exists('.env'):
        print("Cant run, '.env' file missing!")
        return

    if os.getenv("NO_RUN", "false").lower() == "true":
        return

    from WebHeroes.WebHeroes import WebHeroes

    WebHeroes.run()


if __name__ == '__main__':
    main()
