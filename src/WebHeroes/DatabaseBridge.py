"""
DatabaseBridge.py

This module defines the `DatabaseBridge` class, which manages the connection to the MySQL database.
The class is implemented as a static class, establishing the connection during initialization and
retrying upon failure with a configurable timeout.

Classes:
    DatabaseBridge: A static class for establishing and managing a MySQL database connection.
"""

from ZLib.StaticClass import StaticClass
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.errors import DatabaseError
import WebHeroes.config as config
from typing import Optional
import time


class DatabaseBridge(StaticClass):
    """
    A static class responsible for establishing and managing a connection to the MySQL database.

    This class attempts to connect to the database during initialization and retries upon failure
    until a successful connection is established. The retry interval is defined by the
    `DATABASE_RECONNECTION_TIMEOUT` setting in the configuration.

    Attributes:
        database (MySQLConnection): The active MySQL connection instance.
    """

    database: Optional[MySQLConnection] = None

    @staticmethod
    def init() -> None:
        """
        Initializes the DatabaseBridge.
        :return:
        """
        while True:
            print("Connecting to DB!", flush=True)

            try:
                DatabaseBridge.database = mysql.connector.connect(
                    host=config.MYSQL_HOST,
                    user=config.MYSQL_USER,
                    password=config.MYSQL_PASSWORD,
                    database=config.MYSQL_DATABASE
                )

                break
            except DatabaseError:
                print(f"Couldn't connect to DB, retrying in {config.DATABASE_RECONNECTION_TIMEOUT}s!", flush=True)
                time.sleep(config.DATABASE_RECONNECTION_TIMEOUT)
