# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self
from typing import Any

# **info: sqlalchemy imports
from sqlalchemy import select

# ** info: users entity
from src.entities.collect_request_entity import CollectRequest

# ** info: users database connection manager import
from src.database.mysql.connection_manager.mysql_connection_manager import CrudManagedSession

# ** info: artifacts imports
from src.artifacts.uuid.uuid_provider import uuid_provider
from src.artifacts.env.configs import configs

__all__: list[str] = ["CollectRequestProvider"]


class CollectRequestProvider:
    def __init__(self: Self):
        self.connection_manager: CrudManagedSession = CrudManagedSession(
            password=configs.database_password,
            database=configs.database_name,
            user=configs.database_user,
            host=configs.database_host,
            port=configs.database_port,
            logs=configs.database_logs,
        )

    def search_collect_request_by_id(self: Self, uuid: str) -> CollectRequest:
        query: Any = select(CollectRequest.uuid, CollectRequest.collect_date, CollectRequest.production_center_id)
        query = query.where(CollectRequest.uuid == uuid)
        search_collect_request_by_id_result: CollectRequest = self.connection_manager.query_session.execute(statement=query).fetchone()
        return search_collect_request_by_id_result

    def store_collect_request(self: Self, collect_date: str, production_center_id: int) -> str:
        uuid: str = uuid_provider.get_str_uuid()
        new_collect_request: CollectRequest = CollectRequest(uuid=uuid, collect_date=collect_date, production_center_id=production_center_id)
        with self.connection_manager as crud_session:
            crud_session.add(new_collect_request)
        return uuid
