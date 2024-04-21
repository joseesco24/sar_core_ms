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

# ** info: stamina imports
from stamina import retry

# ** info: users entity
from src.modules.user.adapters.database_providers_entities.user_entity import User

# ** info: sidecards.database_managers imports
from src.sidecard.system.database_managers.mysql_manager import MySQLManager

# ** info: sidecards.artifacts imports
from src.sidecard.system.artifacts.datetime_provider import DatetimeProvider
from src.sidecard.system.artifacts.uuid_provider import UuidProvider
from src.sidecard.system.artifacts.env_provider import EnvProvider

# ** info: cachetools imports
from cachetools import TTLCache
from cachetools import cached

__all__: list[str] = ["UserProvider"]

# ** info: creating a shared cache for all the waste provider instances
user_provider_cache: TTLCache = TTLCache(ttl=240, maxsize=20)


class UserProvider:
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

    def clear_cache(self: Self) -> None:
        user_provider_cache.clear()

    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def create_user_with_basic_info(self: Self, email: str, name: str, last_name: str) -> User:
        logging.debug("creating new user with basic info")
        session: Session = self._session_manager.obtain_session()
        uuid: str = self._uuid_provider.get_str_uuid()
        date_time: datetime = self._datetime_provider.get_current_time()
        new_user: User = User(uuid=uuid, active=True, email=email, name=name, last_name=last_name, create=date_time, update=date_time)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        self.clear_cache()
        logging.debug("new user with basic info created")
        return new_user

    @cached(user_provider_cache)
    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def search_user_by_email(self: Self, email: str) -> User:
        logging.debug(f"searching user by email {email}")
        session: Session = self._session_manager.obtain_session()
        query: Any = select(User).where(User.email == email)
        query_result: User = session.exec(statement=query).first()
        logging.debug("searching user by email ended")
        return query_result
