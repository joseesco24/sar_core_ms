# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Union
from typing import Self
from typing import Any

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: users entity
from entities.waste_entity import Waste

# ** info: artifacts imports
from src.artifacts.uuid.uuid_provider import uuid_provider
from src.artifacts.env.configs import configs

# ** info: session managers imports
from src.database.session_managers.mysql_sar_manager import MySQLSarManager

__all__: list[str] = ["WasteProvider"]


class WasteProvider:
    def __init__(self: Self) -> None:
        self._session_manager: MySQLSarManager = MySQLSarManager(
            password=configs.database_password,
            database=configs.database_name,
            username=configs.database_user,
            drivername=r"mysql+pymysql",
            host=configs.database_host,
            port=configs.database_port,
            query={"charset": "utf8"},
        )

    def search_waste_by_id(self: Self, uuid: str) -> Waste:
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Waste).where(Waste.uuid == uuid)
        search_waste_by_id_result: Waste = session.exec(statement=query).first()
        return search_waste_by_id_result

    def store_waste(
        self: Self,
        request_uuid: str,
        type: int,
        packaging: int,
        weight_in_kg: float,
        volume_in_l: float,
        description: str,
        note: Union[str, None] = None,
    ) -> str:
        session: Session = self._session_manager.obtain_session()
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


# ** info: editar esto al trabajar la tajada de los residuos
