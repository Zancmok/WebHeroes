from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Leek.Models.UserModel import UserModel
from Leek.Leek import Leek
from ZancmokLib.StaticClass import StaticClass
from WebHeroes.UserManagement.UserAlreadyExistsError import UserAlreadyExistsError


class UserRepository(StaticClass):
    @staticmethod
    def create_user(username: str, password_hash: str) -> UserModel:
        with Session(Leek.engine) as session:
            user: UserModel = UserModel(
                username=username,
                password_hash=password_hash
            )

            session.add(user)

            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                raise UserAlreadyExistsError

            session.refresh(user)

            return user

    @staticmethod
    def get_by_username(username: str) -> Optional[UserModel]:
        with Session(Leek.engine) as session:
            return session.execute(select(UserModel).where(UserModel.username == username)).scalars().first()
