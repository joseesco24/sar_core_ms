# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import List
from typing import Self
from typing import Any

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: users entity
from src.modules.parameter.adapters.database_providers_entities.parameter_entity import Parameter

# ** info: artifacts imports
from src.sidecards.artifacts.env_provider import EnvProvider

# ** info: session managers imports
from src.sidecards.database_managers.mysql_manager import MySQLManager

__all__: list[str] = ["ParameterProvider"]


class ParameterProvider:
    def __init__(self: Self) -> None:
        self._env_provider: EnvProvider = EnvProvider()
        self._session_manager: MySQLManager = MySQLManager(
            password=self._env_provider.database_password,
            database=self._env_provider.database_name,
            username=self._env_provider.database_user,
            host=self._env_provider.database_host,
            port=self._env_provider.database_port,
            drivername=r"mysql+pymysql",
            query={"charset": "utf8"},
        )

    def search_parameters_by_domain(self: Self, domain: str) -> List[Parameter]:
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Parameter).where(Parameter.domain == domain)
        search_one_collect_request_result: List[Parameter] = session.exec(statement=query).fetchall()
        return search_one_collect_request_result
