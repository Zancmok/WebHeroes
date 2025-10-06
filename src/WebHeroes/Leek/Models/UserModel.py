from Leek.Models.BaseModel import BaseModel
from typing import Optional
from sqlalchemy import Table, Column, Integer, String
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
