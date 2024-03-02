# !/usr/bin/python3
# type: ignore

# ** info: python imports
from datetime import datetime

# ** info: sqlmodel imports
from sqlmodel import SQLModel
from sqlmodel import Field


__all__: list[str] = ["Parameter"]


class Parameter(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    __tablename__: str = "parameter"

    id: int = Field(default=None, primary_key=True)
    domain: str = Field(max_length=40, nullable=False)
    order: int = Field(nullable=False)
    value: str = Field(max_length=40, nullable=False)
    description: str = Field(max_length=65535, nullable=False)
    active: bool = Field(nullable=False)
    create: datetime = Field(nullable=False)
    update: datetime = Field(nullable=False)
