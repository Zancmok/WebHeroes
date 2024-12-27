from ZLib.StaticClass import StaticClass
from ZLib.Console import Console
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.errors import DatabaseError
import WebHeroes.config as config
import time


class DatabaseBridge(StaticClass):
    database: MySQLConnection

    while True:
        Console.print("Connecting to DB!")

        try:
            database = mysql.connector.connect(
                host=config.MYSQL_HOST,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DATABASE
            )

            break
        except DatabaseError:
            Console.warn(f"Couldn't connect to DB, retrying in {config.DATABASE_RECONNECTION_TIMEOUT}s!")
            time.sleep(config.DATABASE_RECONNECTION_TIMEOUT)
