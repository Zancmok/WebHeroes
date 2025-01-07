"""
config.py

This module contains configuration constants and environment variables used throughout the application.
It leverages the `dotenv` package to load sensitive data from a `.env` file and sets up various application settings.

Attributes:
    DEBUG (bool): Enables or disables debug mode for the application.
    PORT (int): The port on which the application runs.
    HOST (str): The host address for the application.
    STATIC_PATH (str): The file path to the static assets' directory.
    TEMPLATES_PATH (str): The file path to the templates' directory.
    SQL_PATH (str): The file path to the SQL scripts directory.
    REDIRECT_URI (str): The OAuth2 redirect URI for the application.
    DISCORD_OAUTH_URL (str): The formatted Discord OAuth2 authorization URL.
    MYSQL_USER (str): The MySQL database username.
    MYSQL_PASSWORD (str): The MySQL database password.
    MYSQL_HOST (str): The MySQL database host.
    MYSQL_DATABASE (str): The name of the MySQL database.
    DISCORD_CLIENT_ID (str): The Discord application client ID.
    DISCORD_CLIENT_SECRET (str): The Discord application client secret.
    DISCORD_BOT_TOKEN (str): The bot token for Discord integration.
    FLASK_SECRET_KEY (str): The secret key for Flask session management.
    DATABASE_RECONNECTION_TIMEOUT (int): Timeout in seconds for reconnecting to the database.
"""

import os
import dotenv
import urllib.parse

dotenv.load_dotenv()

DEBUG: bool = True
PORT: int = 5000
HOST: str = "0.0.0.0"
STATIC_PATH: str = "../static"
TEMPLATES_PATH: str = "../templates"
SQL_PATH: str = "../sql"
REDIRECT_URI: str = "http://localhost:5000/oauth"
DISCORD_OAUTH_URL: str = f"https://discord.com/oauth2/authorize?client_id=1313095758970486799&response_type=code&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&scope=identify"
MYSQL_USER: str = "user"
MYSQL_PASSWORD: str = "password"
MYSQL_HOST: str = "web_heroes_database"
MYSQL_DATABASE: str = "WebHeroes"
DISCORD_CLIENT_ID: str = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET: str = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_BOT_TOKEN: str = os.getenv("DISCORD_BOT_TOKEN")
FLASK_SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY")
DATABASE_RECONNECTION_TIMEOUT: int = 1
