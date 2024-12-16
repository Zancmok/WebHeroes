from ZLib.StaticClass import StaticClass
import mysql.connector
import WebHeroes.config as config


class DatabaseBridge(StaticClass):
    database: mysql.connector.MySQLConnection = mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DATABASE
    )
