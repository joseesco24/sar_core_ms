# !/usr/bin/python3
# type: ignore

# ** info: python imports
import logging
import gc

# ** info: typing imports
from typing import Self

# **info: sqlalchemy imports
from sqlalchemy import text
from sqlalchemy import URL

# ** info: sqlmodel imports
from sqlmodel import create_engine
from sqlmodel import Session

# ** info: artifacts imports
from src.artifacts.uuid.uuid_provider import uuid_provider

# ** info: artifacts imports
from src.artifacts.datetime.datetime_provider import datetime_provider
from src.artifacts.env.configs import configs

__all__: list[str] = ["MySQLSarManager"]


class MySQLSarManager:
    instances: set = set()

    def __init__(self: Self, password: str, database: str, username: str, drivername: str, host: str, port: int, query: dict) -> None:
        self._url = URL(
            drivername=drivername,
            password=password,
            database=database,
            username=username,
            query=query,
            host=host,
            port=port,
        )
        self._engine = create_engine(url=self._url, echo=configs.database_logs)
        self._session_creation: str = datetime_provider.get_utc_iso_string()
        self._connection_id: str = uuid_provider.get_str_uuid()
        self._session = Session(bind=self._engine)
        self._post_init()

    def obtain_session(self: Self) -> Session:
        instanes_ids: str = r",".join(str(s) for s in MySQLSarManager.instances)
        instances_count: int = MySQLSarManager.instances.__len__()
        logging.info("obtaining connection")
        logging.debug(f"instances count: {instances_count}")
        logging.debug(f"instances ids: {instanes_ids}")
        self._check_session_health()
        return self._session

    def _check_session_health(self: Self) -> None:
        is_connection_healthy: bool
        try:
            self._session.exec(text(r"select 1"))
            is_connection_healthy = True
        except Exception as e:
            print(e)
            is_connection_healthy = False
        if is_connection_healthy is False:
            logging.critical(f"connection {self._connection_id} is unhealthy")
            self._restart_session()
            logging.info(f"new connection {self._connection_id} is healthy")
        else:
            logging.info(f"connection {self._connection_id} is healthy")

    def _restart_session(self: Self) -> None:
        logging.warning("restarting connection")
        self._end_session_and_engine()
        self._start_session_and_engine()
        logging.warning("connection restarted")

    def _end_session_and_engine(self: Self) -> None:
        logging.warning(f"ending connection {self._connection_id}")
        if self._session is not None:
            self._session.close()
            del self._session
            gc.collect()
            self._session = None
        if self._engine is not None:
            self._engine.dispose()
            del self._engine
            gc.collect()
            self._engine = None
        logging.warning(f"connection {self._connection_id} ended")
        MySQLSarManager.instances.remove(self._connection_id)

    def _start_session_and_engine(self: Self) -> None:
        self._connection_id = uuid_provider.get_str_uuid()
        logging.warning(f"starting new connection {self._connection_id}")
        if self._engine is None:
            self._engine = create_engine(self._url, echo=configs.database_logs)
        if self._session is None:
            self._session = Session(bind=self._engine)
        logging.warning(f"new connection {self._connection_id} started")

    def _post_init(self: Self) -> None:
        logging.info(f"connection started with id {self._connection_id}")
        MySQLSarManager.instances.add(self._connection_id)
