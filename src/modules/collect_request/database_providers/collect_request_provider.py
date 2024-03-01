# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self
from typing import Any

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: users entity
from src.modules.collect_request.entities.collect_request_entity import CollectRequest

# ** info: artifacts imports
from src.sidecards.uuid.uuid_provider import uuid_provider
from src.sidecards.env.configs import configs

# ** info: session managers imports
from src.modules.database.session_managers.mysql_sar_manager import MySQLSarManager

__all__: list[str] = ["CollectRequestProvider"]


class CollectRequestProvider:
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

    def search_collect_request_by_id(self: Self, uuid: str) -> CollectRequest:
        session: Session = self._session_manager.obtain_session()
        query: Any = select(CollectRequest).where(CollectRequest.uuid == uuid)
        search_collect_request_by_id_result: CollectRequest = session.exec(statement=query).first()
        return search_collect_request_by_id_result

    def store_collect_request(self: Self, collect_date: str, production_center_id: int) -> str:
        session: Session = self._session_manager.obtain_session()
        uuid: str = uuid_provider.get_str_uuid()
        new_collect_request: CollectRequest = CollectRequest(uuid=uuid, collect_date=collect_date, production_center_id=production_center_id)
        session.add(new_collect_request)
        session.commit()
        return uuid
