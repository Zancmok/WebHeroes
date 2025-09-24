from typing import Optional

from ZancmokLib.StaticClass import StaticClass
from WebHeroes.UserManagement.User import User
from WebHeroes.UserManagement.UserFactory import UserFactory


class UserAccountManager(StaticClass):
    @staticmethod
    def create_account(username: str, password: str) -> Optional[User]:
        ...

    @staticmethod
    def try_login(username: str, password: str) -> Optional[User]:
        ...
