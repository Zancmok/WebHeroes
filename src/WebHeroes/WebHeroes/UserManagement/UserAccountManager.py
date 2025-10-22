from typing import Optional

from ZancmokLib.StaticClass import StaticClass
from WebHeroes.UserManagement.SessionManager import SessionManager
from WebHeroes.UserManagement.Errors.UserAlreadyExistsError import UserAlreadyExistsError
from WebHeroes.UserManagement.Errors.InvalidUsernameError import InvalidUsernameError
from WebHeroes.UserManagement.Errors.UserDoesntExistError import UserDoesntExistError
from WebHeroes.UserManagement.Errors.AuthFailedError import AuthFailedError
from WebHeroes.UserManagement.Errors.AlreadyLoggedInError import AlreadyLoggedInError
from WebHeroes.Errors.NotLoggedInError import NotLoggedInError
from Leek.Repositories.UserRepository import UserRepository
from Leek.Models.UserModel import UserModel
import bcrypt


class UserAccountManager(StaticClass):
    @staticmethod
    def create_account(username: str, password: str) -> UserModel:
        allowed_letters: str = "abcdefghijklmnoprstuvzxywqABCDEFGHIJKLMNOPRSTUVZQXYW0123456789_-"

        if len(username) not in range(3, 17):
            raise InvalidUsernameError("Username must be between '3' and '16' characters long!")

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
        user: Optional[UserModel] = UserRepository.get_by_username(username)

        if not user:
            raise UserDoesntExistError(f"User '{username}' doesn't exist.")

        if old_user_id := SessionManager.get_user_id():
            old_user_id: int

            if old_user_id == user.id:
                return user
            else:
                raise AlreadyLoggedInError(f"You are already logged in as another user.")

        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            raise AuthFailedError(f"Password incorrect.")

        SessionManager.new_session(user.id)

        return user

    @staticmethod
    def try_logout(token: Optional[str] = None) -> None:
        if not SessionManager.get_user_id():
            raise NotLoggedInError
        
        SessionManager.kill_session(token)
