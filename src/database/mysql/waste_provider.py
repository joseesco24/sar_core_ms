# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Union
from typing import Self
from typing import Any

# **info: sqlalchemy imports
from sqlalchemy import select

# ** info: users entity
from entities.waste_entity import Waste

# ** info: users database connection manager import
from src.database.mysql.connection_manager.mysql_connection_manager import CrudManagedSession

# ** info: artifacts imports
from src.artifacts.uuid.uuid_provider import uuid_provider
from src.artifacts.env.configs import configs

__all__: list[str] = ["WasteProvider"]


class WasteProvider:
    def __init__(self: Self):
        self.connection_manager: CrudManagedSession = CrudManagedSession(
            password=configs.database_password,
            database=configs.database_name,
            user=configs.database_user,
            host=configs.database_host,
            port=configs.database_port,
            logs=configs.database_logs,
        )

    def search_waste_by_id(self: Self, uuid: str) -> Waste:
        query: Any = select(
            Waste.uuid, Waste.request_uuid, Waste.type, Waste.packaging, Waste.weight_in_kg, Waste.volume_in_l, Waste.description, Waste.note
        )
        query = query.where(Waste.uuid == uuid)
        search_waste_by_id_result: Waste = self.connection_manager.query_session.execute(statement=query).fetchone()
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
        with self.connection_manager as crud_session:
            crud_session.add(new_waste)
        return uuid
