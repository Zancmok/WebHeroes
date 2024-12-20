import os


def main() -> None:
    """
    Runs the main class.
    :return:
    """
    if not os.path.exists('.env'):
        print("Cant run, '.env' file missing!")
        return

    if os.getenv("NO_RUN", "false").lower() == "true":
        return

    from WebHeroes.WebHeroes import WebHeroes

    WebHeroes.run()


if __name__ == '__main__':
    main()
