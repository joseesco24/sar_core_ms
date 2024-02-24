# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Union
from typing import Any

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: users entity
from entities.waste_entity import Waste

# ** info: artifacts imports
from src.artifacts.uuid.uuid_provider import uuid_provider

# ** info: session managers imports
from src.database.session_managers.mysql_sar_manager import mysql_sar_manager

__all__: list[str] = ["WasteProvider"]


class WasteProvider:
    @staticmethod
    def search_waste_by_id(uuid: str) -> Waste:
        session: Session = mysql_sar_manager.obtain_session()
        query: Any = select(Waste).where(Waste.uuid == uuid)
        search_waste_by_id_result: Waste = session.exec(statement=query).first()
        return search_waste_by_id_result

    @staticmethod
    def store_waste(
        request_uuid: str,
        type: int,
        packaging: int,
        weight_in_kg: float,
        volume_in_l: float,
        description: str,
        note: Union[str, None] = None,
    ) -> str:
        session: Session = mysql_sar_manager.obtain_session()
        uuid: str = uuid_provider.get_str_uuid()
        new_waste: Waste = Waste(
            uuid=uuid,
            request_uuid=request_uuid,
            type=type,
            packaging=packaging,
            weight_in_kg=weight_in_kg,
            volume_in_l=volume_in_l,
            description=description,
            note=note,
        )
        session.add(new_waste)
        session.commit()
        return uuid
