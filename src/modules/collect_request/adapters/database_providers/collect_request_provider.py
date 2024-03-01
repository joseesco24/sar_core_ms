# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self
from typing import Any

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: users entity
from src.modules.collect_request.adapters.database_providers_entities.collect_request_entity import CollectRequest

# ** info: artifacts imports
from src.sidecards.artifacts.uuid_provider import UuidProvider
from src.sidecards.artifacts.env_provider import EnvProvider

# ** info: session managers imports
from src.sidecards.database_managers.mysql_manager import MySQLManager

__all__: list[str] = ["CollectRequestProvider"]


class CollectRequestProvider:
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

    def search_collect_request_by_id(self: Self, uuid: str) -> CollectRequest:
        session: Session = self._session_manager.obtain_session()
        query: Any = select(CollectRequest).where(CollectRequest.uuid == uuid)
        search_collect_request_by_id_result: CollectRequest = session.exec(statement=query).first()
        return search_collect_request_by_id_result

    def store_collect_request(self: Self, collect_date: str, production_center_id: int) -> str:
        session: Session = self._session_manager.obtain_session()
        uuid: str = self._uuid_provider.get_str_uuid()
        new_collect_request: CollectRequest = CollectRequest(uuid=uuid, collect_date=collect_date, production_center_id=production_center_id)
        session.add(new_collect_request)
        session.commit()
        return uuid
