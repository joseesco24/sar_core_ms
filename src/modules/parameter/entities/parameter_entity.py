# !/usr/bin/python3
# type: ignore

# ** info: sqlmodel imports
from sqlmodel import SQLModel
from sqlmodel import Field


__all__: list[str] = ["Parameter"]


class Parameter(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    __tablename__: str = "parameter"

    id: int = Field(default=None, primary_key=True)
    domain: str = Field(max_length=40, nullable=False)
    value: str = Field(max_length=40, nullable=False)
    description: str = Field(max_length=65535, nullable=False)
    active: bool = Field(nullable=False)
