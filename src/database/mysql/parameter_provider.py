# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import List
from typing import Self
from typing import Any

# **info: sqlalchemy imports
from sqlalchemy import select

# ** info: users entity
from src.entities.parameter_entity import Parameter

# ** info: users database connection manager import
from src.database.mysql.connection_manager.mysql_connection_manager import CrudManagedSession

# ** info: artifacts imports
from src.artifacts.env.configs import configs

__all__: list[str] = ["ParameterProvider"]


class ParameterProvider:
    def __init__(self: Self):
        self.connection_manager: CrudManagedSession = CrudManagedSession(
            password=configs.database_password,
            database=configs.database_name,
            user=configs.database_user,
            host=configs.database_host,
            port=configs.database_port,
            logs=configs.database_logs,
        )

    def search_parameters_by_domain(self: Self, domain: str) -> List[Parameter]:
        search_one_collect_request_result: List[Parameter]
        query: Any = select(Parameter.id, Parameter.domain, Parameter.value, Parameter.description, Parameter.active)
        query = query.where(Parameter.domain == domain)
        search_one_collect_request_result: List[Parameter] = self.connection_manager.query_session.execute(statement=query).fetchmany()
        return search_one_collect_request_result
