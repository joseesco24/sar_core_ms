# !/usr/bin/python3
# type: ignore

# ** info: sqlalchemy imports
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Text

# ** info: sqlalchemy declarative imports
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

__all__: list[str] = ["Parameter"]


class Parameter(Base):
    __tablename__: str = "parameter"

    id: Column = Column(Integer, primary_key=True)
    domain: Column = Column(String(40), unique=True)
    value: Column = Column(String(40), unique=True)
    description: Column = Column(Text)
    active: Column = Column(Boolean)
