# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Any

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: users entity
from src.entities.collect_request_entity import CollectRequest

# ** info: artifacts imports
from src.artifacts.uuid.uuid_provider import uuid_provider

# ** info: session managers imports
from src.database.session_managers.mysql_sar_manager import MySQLSarManager

__all__: list[str] = ["CollectRequestProvider"]


class CollectRequestProvider:
    @staticmethod
    def search_collect_request_by_id(uuid: str) -> CollectRequest:
        session: Session = MySQLSarManager.obtain_session()
        query: Any = select(CollectRequest).where(CollectRequest.uuid == uuid)
        search_collect_request_by_id_result: CollectRequest = session.exec(statement=query).first()
        return search_collect_request_by_id_result

    @staticmethod
    def store_collect_request(collect_date: str, production_center_id: int) -> str:
        session: Session = MySQLSarManager.obtain_session()
        uuid: str = uuid_provider.get_str_uuid()
        new_collect_request: CollectRequest = CollectRequest(uuid=uuid, collect_date=collect_date, production_center_id=production_center_id)
        session.add(new_collect_request)
        session.commit()
        return uuid
