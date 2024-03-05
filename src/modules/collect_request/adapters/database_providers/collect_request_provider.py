# !/usr/bin/python3
# type: ignore

# ** info: python imports
from datetime import datetime
import logging

# ** info: typing imports
from typing import Self
from typing import Any

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: users entity
from src.modules.collect_request.adapters.database_providers_entities.collect_request_entity import (
    CollectRequest,
)

# ** info: sidecards imports
from src.sidecards.artifacts.datetime_provider import DatetimeProvider
from src.sidecards.database_managers.mysql_manager import MySQLManager
from src.sidecards.artifacts.uuid_provider import UuidProvider
from src.sidecards.artifacts.env_provider import EnvProvider

# ** info: cachetools imports
from cachetools import TTLCache
from cachetools import cached

__all__: list[str] = ["CollectRequestProvider"]


class CollectRequestProvider:
    def __init__(self: Self) -> None:
        self._env_provider: EnvProvider = EnvProvider()
        self._uuid_provider: UuidProvider = UuidProvider()
        self._datetime_provider: DatetimeProvider = DatetimeProvider()
        self._session_manager: MySQLManager = MySQLManager(
            password=self._env_provider.database_password,
            database=self._env_provider.database_name,
            username=self._env_provider.database_user,
            host=self._env_provider.database_host,
            port=self._env_provider.database_port,
            drivername=r"mysql+pymysql",
            query={"charset": "utf8"},
        )

    @cached(cache=TTLCache(ttl=60, maxsize=20))
    def search_collect_request_by_id(self: Self, uuid: str) -> CollectRequest:
        logging.debug(f"searching collect request by id {uuid}")
        session: Session = self._session_manager.obtain_session()
        query: Any = select(CollectRequest).where(CollectRequest.uuid == uuid)
        search_collect_request_by_id_result: CollectRequest = session.exec(statement=query).first()
        logging.debug("searching collect request by id ended")
        return search_collect_request_by_id_result

    def store_collect_request(self: Self, collect_date: str, production_center_id: int) -> CollectRequest:
        logging.debug("creating a new collect request")
        session: Session = self._session_manager.obtain_session()
        uuid: str = self._uuid_provider.get_str_uuid()
        date_time: datetime = self._datetime_provider.get_current_time()
        new_collect_request: CollectRequest = CollectRequest(
            production_center_id=production_center_id,
            collect_date=collect_date,
            process_status=9,
            create=date_time,
            update=date_time,
            uuid=uuid,
        )
        session.add(new_collect_request)
        session.commit()
        session.refresh(new_collect_request)
        logging.debug("new collect request created")
        return new_collect_request
