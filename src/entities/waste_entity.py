# !/usr/bin/python3
# type: ignore

# ** info: python imports
from decimal import Decimal

# ** info: typing imports
from typing import Optional

# ** info: sqlmodel imports
from sqlmodel import SQLModel
from sqlmodel import Field


class Waste(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "waste"

    uuid: str = Field(max_length=36, primary_key=True)
    request_uuid: str = Field(max_length=36, nullable=False)
    type: int = Field(nullable=False)
    packaging: int = Field(nullable=False)
    weight_in_kg: Decimal = Field(max_digits=10, decimal_places=2, nullable=False)
    volume_in_l: Decimal = Field(max_digits=10, decimal_places=2, nullable=False)
    isotopes_number: Decimal = Field(max_digits=10, decimal_places=2, nullable=True)
    state_waste: int = Field(nullable=True)
    store: int = Field(nullable=True)
    description: str = Field(max_length=65535, nullable=False)
    note: Optional[str] = Field(max_length=65535, nullable=False)


# ** info: editar esto al trabajar la tajada de los residuos
