DEBUG: bool = True
PORT: int = 5000
HOST: str = "0.0.0.0"
STATIC_PATH: str = "../static"
TEMPLATES_PATH: str = "../templates"
DISCORD_OAUTH_URL: str = r"https://discord.com/oauth2/authorize?client_id=1313095758970486799&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Foauth&scope=identify"

import os
import dotenv

dotenv.load_dotenv()

DISCORD_CLIENT_ID: str = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET: str = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_BOT_TOKEN: str = os.getenv("DISCORD_BOT_TOKEN")
