# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import List
from typing import Any

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: users entity
from src.entities.parameter_entity import Parameter

# ** info: session managers imports
from src.database.session_managers.mysql_sar_manager import MySQLSarManager

__all__: list[str] = ["ParameterProvider"]


class ParameterProvider:
    @staticmethod
    def search_parameters_by_domain(domain: str) -> List[Parameter]:
        session: Session = MySQLSarManager.obtain_session()
        query: Any = select(Parameter).where(Parameter.domain == domain)
        search_one_collect_request_result: List[Parameter] = session.exec(statement=query).fetchall()
        return search_one_collect_request_result
