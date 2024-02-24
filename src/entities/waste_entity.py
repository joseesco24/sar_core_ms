# !/usr/bin/python3
# type: ignore

# ** info: sqlalchemy imports
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Text

# ** info: sqlalchemy declarative imports
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

__all__: list[str] = ["Waste"]


class Waste(Base):
    __tablename__ = "waste"

    uuid = Column(String(36), primary_key=True)
    request_uuid = Column(String(36))
    type = Column(Integer)
    packaging = Column(Integer)
    weight_in_kg = Column(Float(10, 2))
    volume_in_l = Column(Float(10, 2))
    description = Column(Text)
    note = Column(Text)
