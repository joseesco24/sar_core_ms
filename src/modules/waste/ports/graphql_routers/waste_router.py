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

# ** info: users dtos imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFilterByStatusRequestDto
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseListDto

# ** info: app core imports
from src.modules.waste.cores.business.waste_core import WasteCore

__all__: list[str] = ["waste_gpl_router"]

# ** info: building router core
_waste_core: WasteCore = WasteCore()

# ** info: building sidecards
_path_provider: PathProvider = PathProvider()
_env_provider: EnvProvider = EnvProvider()

# ---------------------------------------------------------------------------------------------------------------------
# ** info: assembling schema literal
# ---------------------------------------------------------------------------------------------------------------------

current_file_path: Path = Path(__file__).parent.resolve()
schema_path: Path = Path(current_file_path, "..", "graphql_routers_dtos", "waste_dtos.graphql")
schema_literal: str = load_schema_from_path(path=str(schema_path))

# ---------------------------------------------------------------------------------------------------------------------
# ** info: assembling querie facades with resolvers
# ---------------------------------------------------------------------------------------------------------------------

query: QueryType = QueryType()


@query.field("wastesByStatus")
async def users_public_data_facade(*_: Any, processStatus: int) -> WasteFullDataResponseListDto:
    filter_waste_by_status_request: WasteFilterByStatusRequestDto = WasteFilterByStatusRequestDto(processStatus=processStatus)
    filtered_wastes_response: WasteFullDataResponseListDto = await _waste_core.driver_search_waste_by_status(filter_waste_by_status_request)
    return filtered_wastes_response.values


# ---------------------------------------------------------------------------------------------------------------------
# ** info: assembling schema literal with schema executable
# ---------------------------------------------------------------------------------------------------------------------

schema_executable: GraphQLSchema = make_executable_schema(schema_literal, query, integer_scalar, float_scalar)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: assembling schema executable with graphql endpoint
# ---------------------------------------------------------------------------------------------------------------------

graphql_endpoint_definition: GraphQL = GraphQL(
    debug=False if _env_provider.app_environment_mode == "production" else True,
    validation_rules=[cost_validator(maximum_cost=5)],
    error_formatter=error_formatter.formatter,
    schema=schema_executable,
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: assembling graphql endpoint with the main router
# ---------------------------------------------------------------------------------------------------------------------

waste_gpl_router: Route = Route(
    path=_path_provider.build_posix_path("waste"),
    endpoint=graphql_endpoint_definition,
)
