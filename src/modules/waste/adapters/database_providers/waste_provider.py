# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Union
from typing import Self
from typing import Any

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: fastapi imports
from fastapi import HTTPException
from fastapi import status

# ** info: users entity
from src.modules.waste.adapters.database_providers_entities.waste_entity import Waste

# ** info: artifacts imports
from src.sidecards.artifacts.uuid_provider import UuidProvider
from src.sidecards.artifacts.env_provider import EnvProvider

# ** info: session managers imports
from src.sidecards.database_managers.mysql_manager import MySQLManager

__all__: list[str] = ["WasteProvider"]


class WasteProvider:
    def __init__(self: Self) -> None:
        self._env_provider: EnvProvider = EnvProvider()
        self._uuid_provider: UuidProvider = UuidProvider()
        self._session_manager: MySQLManager = MySQLManager(
            password=self._env_provider.database_password,
            database=self._env_provider.database_name,
            username=self._env_provider.database_user,
            host=self._env_provider.database_host,
            port=self._env_provider.database_port,
            drivername=r"mysql+pymysql",
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
        uuid: str = self._uuid_provider.get_str_uuid()
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

    def classify_waste(self: Self, uuid: str, isotopes_number: float, state_waste: int, store: int) -> int:
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Waste).where(Waste.uuid == uuid)
        wasteResult = session.exec(statement=query).first()
        if wasteResult is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="waste not found")
        wasteResult.isotopes_number = isotopes_number
        wasteResult.state_waste = state_waste
        wasteResult.store = store
        session.add(wasteResult)
        session.commit()
        code: int = 1
        return code
