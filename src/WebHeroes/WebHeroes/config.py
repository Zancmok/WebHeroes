import os

import dotenv

dotenv.load_dotenv()

DEBUG: bool = True
PORT: int = 5000
HOST: str = "0.0.0.0"
STATIC_PATH: str = "../static"
TEMPLATES_PATH: str = "../templates"
SQL_PATH: str = "../Leek/scripts"
MYSQL_USER: str = "user"
MYSQL_PASSWORD: str = "password"
MYSQL_HOST: str = "web_heroes_database"
MYSQL_DATABASE: str = "WebHeroes"
FLASK_SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY")
DATABASE_RECONNECTION_TIMEOUT: int = 1
