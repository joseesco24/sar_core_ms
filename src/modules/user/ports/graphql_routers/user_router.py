# !/usr/bin/python3
# type: ignore

# ** info: python imports
from pathlib import Path

# ** info: typing imports
from typing import Any

# ** info: starlette imports
from starlette.routing import Route

# ** info: graphql imports
from graphql import GraphQLSchema

# ** info: ariadne imports
from ariadne.validation import cost_validator
from ariadne import make_executable_schema
from ariadne import load_schema_from_path
from ariadne.asgi import GraphQL
from ariadne import QueryType

# ** info: artifacts imports
from src.general_sidecards.graphql.custom_scalars_serializer import integer_scalar
from src.general_sidecards.graphql.custom_scalars_serializer import float_scalar
from src.general_sidecards.graphql.error_formatter import error_formatter
from src.general_sidecards.artifacts.path_provider import PathProvider
from src.general_sidecards.artifacts.env_provider import EnvProvider

# ** info: dtos imports
from src.modules.user.ports.rest_routers_dtos.user_dtos import UserCreationResponseDto  # type: ignore
from src.modules.user.ports.rest_routers_dtos.user_dtos import UserByEmailRequestDto  # type: ignore

# ** info: app core imports
from src.modules.user.core.business.user_core import UserCore

__all__: list[str] = ["user_gpl_router"]

# ** info: building router core
_user_core: UserCore = UserCore()

# ** info: building sidecards
_path_provider: PathProvider = PathProvider()
_env_provider: EnvProvider = EnvProvider()

# ---------------------------------------------------------------------------------------------------------------------
# ** info: assembling schema literal
# ---------------------------------------------------------------------------------------------------------------------

current_file_path: Path = Path(__file__).parent.resolve()
schema_path: Path = Path(current_file_path, "..", "graphql_routers_dtos", "user_dtos.graphql")
schema_literal: str = load_schema_from_path(path=str(schema_path))

# ---------------------------------------------------------------------------------------------------------------------
# ** info: assembling querie facades with resolvers
# ---------------------------------------------------------------------------------------------------------------------

query: QueryType = QueryType()


@query.field("userByEmail")
async def user_by_email(*_: Any, email: str) -> UserCreationResponseDto:
    user_by_email_request: UserByEmailRequestDto = UserByEmailRequestDto(email=email)
    user_full_data_reponse: UserCreationResponseDto = await _user_core.driver_get_user_by_email(user_by_email_request)
    return user_full_data_reponse


# ---------------------------------------------------------------------------------------------------------------------
# ** info: assembling schema literal with schema executable
# ---------------------------------------------------------------------------------------------------------------------

schema_executable: GraphQLSchema = make_executable_schema(schema_literal, query, integer_scalar, float_scalar)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: assembling schema executable with graphql endpoint
# ---------------------------------------------------------------------------------------------------------------------

graphql_endpoint_definition: GraphQL = GraphQL(
    introspection=False if _env_provider.app_environment_mode == "production" else True,
    debug=False if _env_provider.app_environment_mode == "production" else True,
    validation_rules=[cost_validator(maximum_cost=5)],
    error_formatter=error_formatter.formatter,
    schema=schema_executable,
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: assembling graphql endpoint with the main router
# ---------------------------------------------------------------------------------------------------------------------

user_gpl_router: Route = Route(
    path=_path_provider.build_posix_path("user"),
    endpoint=graphql_endpoint_definition,
)
