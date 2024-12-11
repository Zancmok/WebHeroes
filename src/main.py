import os
from WebHeroes.WebHeroes import WebHeroes


def main() -> None:
    """
    Runs the main class.
    :return:
    """
    if not os.path.exists('.env'):
        print("Cant run, '.env' file missing!")
        return

    WebHeroes.run()


if __name__ == '__main__':
    main()
