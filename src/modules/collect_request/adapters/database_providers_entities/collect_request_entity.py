# !/usr/bin/python3
# type: ignore

# ** info: python imports
from datetime import datetime

# ** info: sqlmodel imports
from sqlmodel import SQLModel
from sqlmodel import Field

__all__: list[str] = ["CollectRequest"]


class CollectRequest(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "collect_request"

    uuid: str = Field(max_length=36, primary_key=True)
    collect_date: datetime = Field(nullable=False)
    process_status: int = Field(nullable=False)
    production_center_id: int = Field(nullable=False)
    create: datetime = Field(nullable=False)
    update: datetime = Field(nullable=False)
