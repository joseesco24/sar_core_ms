# !/usr/bin/python3
# type: ignore

# ** info: python imports
from datetime import datetime

# ** info: sqlmodel imports
from sqlmodel import SQLModel
from sqlmodel import Field


class User(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "user"

    uuid: str = Field(max_length=36, primary_key=True)
    active: bool = Field(nullable=False)
    email: str = Field(max_length=200, nullable=False, unique=True)
    name: str = Field(max_length=200, nullable=False)
    last_name: str = Field(max_length=200, nullable=False)
    create: datetime = Field(nullable=False)
    update: datetime = Field(nullable=False)
