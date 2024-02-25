# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self

# **info: sqlalchemy imports
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
    def obtain_session(self: Self) -> Session:
        return self._session
