from ZancmokLib.StaticClass import StaticClass
from WebHeroes.UserManagement.Errors.UserAlreadyExistsError import UserAlreadyExistsError
from WebHeroes.UserManagement.Errors.InvalidUsernameError import InvalidUsernameError
from Leek.Repositories.UserRepository import UserRepository
from Leek.Models.UserModel import UserModel
import bcrypt


class UserAccountManager(StaticClass):
    @staticmethod
    def create_account(username: str, password: str) -> UserModel:
        allowed_letters: str = "abcdefghijklmnoprstuvzxywqABCDEFGHIJKLMNOPRSTUVZQXYW0123456789_-"

        for letter in username:
            if letter not in allowed_letters:
                raise InvalidUsernameError(f"Letter '{letter}' is not allowed inside of a username.")

        password_bytes: bytes = password.encode()
        password_hash: bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        try:
            user: UserModel = UserRepository.create_user(
                username=username,
                password_hash=password_hash.decode()
            )
        except UserAlreadyExistsError:
            raise UserAlreadyExistsError(f"Username '{username}' already exists.")

        return user

    @staticmethod
    def try_login(username: str, password: str) -> UserModel:
        ...
