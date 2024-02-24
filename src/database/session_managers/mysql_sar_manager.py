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

__all__: list[str] = ["mysql_sar_manager"]


class MySQLSarManager:
    def __init__(self: Self):
        url = URL(
            password=configs.database_password,
            database=configs.database_name,
            username=configs.database_user,
            drivername=r"mysql+pymysql",
            host=configs.database_host,
            port=configs.database_port,
            query={"charset": "utf8"},
        )
        self._engine = create_engine(url)
        self._session = Session(bind=self._engine)

    def obtain_session(self: Self) -> Session:
        return self._session


mysql_sar_manager: MySQLSarManager = MySQLSarManager()
