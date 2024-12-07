import os
import dotenv
import urllib.parse

dotenv.load_dotenv()

DEBUG: bool = True
PORT: int = 5000
HOST: str = "0.0.0.0"
STATIC_PATH: str = "../static"
TEMPLATES_PATH: str = "../templates"
REDIRECT_URI: str = "http://localhost:5000/oauth"
DISCORD_OAUTH_URL: str = f"https://discord.com/oauth2/authorize?client_id=1313095758970486799&response_type=code&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&scope=identify"
DISCORD_CLIENT_ID: str = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET: str = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_BOT_TOKEN: str = os.getenv("DISCORD_BOT_TOKEN")
FLASK_SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY")
