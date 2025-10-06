from typing import Optional

from ZancmokLib.StaticClass import StaticClass
from WebHeroes.UserManagement.UserFactory import UserFactory
from Leek.Repositories.UserRepository import UserRepository
from Leek.Models.UserModel import UserModel


class UserAccountManager(StaticClass):
    @staticmethod
    def create_account(username: str, password: str) -> UserModel:
        user: UserModel = UserRepository.create_user(
            username=username,
            password_hash=password  # TODO: Implement encription with bcrypt!!!!
        )

        return user

    @staticmethod
    def try_login(username: str, password: str) -> UserModel:
        ...
