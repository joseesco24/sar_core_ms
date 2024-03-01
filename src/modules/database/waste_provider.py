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
from src.modules.entities.waste_entity import Waste

# ** info: artifacts imports
from src.sidecards.uuid.uuid_provider import uuid_provider
from src.sidecards.env.configs import configs

# ** info: session managers imports
from src.modules.database.session_managers.mysql_sar_manager import MySQLSarManager

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

    def classify_waste(self: Self, uuid: str, isotopes_number: float, state_waste: int, store: int) -> str:
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Waste).where(Waste.uuid == uuid)
        wasteResult = session.exec(statement=query).first()
        print("Residuo:", wasteResult)
        wasteResult.isotopes_number = isotopes_number
        wasteResult.state_waste = state_waste
        wasteResult.store = store
        session.add(wasteResult)
        session.commit()
        session.refresh(wasteResult)
        print("Updated Residuo:", wasteResult)
        code: int = 1
        return code


# ** info: editar esto al trabajar la tajada de los residuos
