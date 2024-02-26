# !/usr/bin/python3
# type: ignore

# ** info: python imports
import logging
import gc

# **info: sqlalchemy imports
from sqlalchemy import text
from sqlalchemy import URL


# ** info: sqlmodel imports
from sqlmodel import create_engine
from sqlmodel import Session

# ** info: artifacts imports
from src.artifacts.env.configs import configs

__all__: list[str] = ["MySQLSarManager"]


class MySQLSarManager:
    _url = URL(
        password=configs.database_password,
        database=configs.database_name,
        username=configs.database_user,
        drivername=r"mysql+pymysql",
        host=configs.database_host,
        port=configs.database_port,
        query={"charset": "utf8"},
    )
    _engine = create_engine(_url, echo=configs.database_logs)
    _session = Session(bind=_engine)

    @classmethod
    def _start_session_and_engine(cls) -> None:
        logging.warning("starting a new connection")
        if cls._engine is None:
            cls._engine = create_engine(cls._url, echo=configs.database_logs)
        if cls._session is None:
            cls._session = Session(bind=cls._engine)
        logging.warning("new connection started")

    @classmethod
    def _end_session_and_engine(cls) -> None:
        logging.warning("ending connection")

        if cls._session is not None:
            cls._session.close()
            del cls._session
            gc.collect()
            cls._session = None

        if cls._engine is not None:
            cls._engine.dispose()
            del cls._engine
            gc.collect()
            cls._engine = None
        logging.warning("connection ended")

    @classmethod
    def _restart_session(cls) -> None:
        logging.warning("restarting connection")
        cls._end_session_and_engine()
        cls._start_session_and_engine()
        logging.warning("connection restarted")

    @classmethod
    def _check_session_health(cls) -> None:
        is_connection_healthy: bool
        try:
            cls._session.exec(text(r"select 1"))
            is_connection_healthy = True
        except Exception as e:
            print(e)
            is_connection_healthy = False
        if is_connection_healthy is False:
            logging.critical("connection is unhealthy")
            cls._restart_session()
            logging.info(f"new connection is healthy: {cls._session.is_active}")
        else:
            logging.info("connection is healthy")

    @classmethod
    def obtain_session(cls) -> Session:
        logging.info("obtaining connection")
        cls._check_session_health()
        return cls._session
