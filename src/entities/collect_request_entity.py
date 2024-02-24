# !/usr/bin/python3
# type: ignore

# ** info: sqlalchemy imports
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Date

# ** info: sqlalchemy declarative imports
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

__all__: list[str] = ["CollectRequest"]


class CollectRequest(Base):
    __tablename__ = "collect_request"

    uuid = Column(String(36), primary_key=True)
    collect_date = Column(Date)
    production_center_id = Column(Integer)
