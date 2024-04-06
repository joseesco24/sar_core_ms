# !/usr/bin/python3
# type: ignore

# ** info: python imports
import logging

# ** info: typing imports
from typing import List
from typing import Self
from typing import Any

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: stamina imports
from stamina import retry

# ** info: users entity
from src.modules.parameter.adapters.database_providers_entities.parameter_entity import Parameter

# ** info: sidecards.database_managers imports
from src.sidecard.system.database_managers.mysql_manager import MySQLManager

# ** info: sidecards.artifacts imports
from src.sidecard.system.artifacts.datetime_provider import DatetimeProvider
from src.sidecard.system.artifacts.env_provider import EnvProvider

# ** info: cachetools imports
from cachetools import TTLCache
from cachetools import cached

__all__: list[str] = ["ParameterProvider"]

# ** info: creating a shared cache for all the parameter provider instances
parameter_provider_cache: TTLCache = TTLCache(ttl=300, maxsize=60)


class ParameterProvider:
    def __init__(self: Self) -> None:
        self._env_provider: EnvProvider = EnvProvider()
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

    def clear_cache(self: Self) -> None:
        parameter_provider_cache.clear()

    @cached(parameter_provider_cache)
    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def search_parameters_by_domain(self: Self, domain: str) -> List[Parameter]:
        logging.debug(f"searching parameters by domain {domain}")
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Parameter).where(Parameter.domain == domain, Parameter.active == True).order_by(Parameter.order)  # noqa: E712
        search_one_collect_request_result: List[Parameter] = session.exec(statement=query).fetchall()
        logging.debug("searching parameters by domain ended")
        return search_one_collect_request_result
