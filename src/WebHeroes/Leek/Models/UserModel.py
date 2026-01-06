from Leek.Models.BaseModel import BaseModel
from WebHeroes.UserManagement.EUserPermissionLevel import EUserPermissionLevel
from typing import Optional
from sqlalchemy import Table, Column, Integer, String, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserModel(BaseModel):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True
    )
    password_hash: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )
    permission_level: Mapped[EUserPermissionLevel] = mapped_column(
        SAEnum(EUserPermissionLevel),
        nullable=False,
        default=EUserPermissionLevel.DEFAULT
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', permission='{self.permission_level.name}')>"
