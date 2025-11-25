import sqlalchemy
from sqlalchemy import Engine, text
from sqlalchemy.exc import OperationalError
from ZancmokLib.StaticClass import StaticClass
from time import sleep
import WebHeroes.config as config
# Models necessary for the metadata creation of them.
from Leek.Models.BaseModel import BaseModel
from Leek.Models.UserModel import UserModel


class Leek(StaticClass):
    engine: Engine = sqlalchemy.create_engine(
        "mysql+pymysql://user:password@web_heroes_database:3306/WebHeroes",
        echo=True
    )

    @staticmethod
    def initialize() -> None:
        while True:
            try:
                with Leek.engine.connect() as conn:
                    result = conn.execute(text("SELECT 'Miku Dayo'"))
                    print(result.all(), flush=True)

                break
            except OperationalError:
                print(f"Retrying connection in {config.DATABASE_RECONNECTION_TIMEOUT}s...", flush=True)
                sleep(config.DATABASE_RECONNECTION_TIMEOUT)

        BaseModel.metadata.create_all(Leek.engine)
