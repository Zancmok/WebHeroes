import os


def main() -> None:
    """
    Runs the main class.
    :return:
    """
    if not os.path.exists('.env'):
        print("Cant run, '.env' file missing!")
        return

    from WebHeroes.WebHeroes import WebHeroes

    WebHeroes.run()


if __name__ == '__main__':
    main()
