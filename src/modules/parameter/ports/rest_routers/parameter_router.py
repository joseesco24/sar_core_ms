# !/usr/bin/python3

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: port dtos imports
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos import ParameterSearchResponseDto  # type: ignore
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos import ParameterSearchRequestDto  # type: ignore

# ** info: app core imports
from src.modules.parameter.cores.business.parameter_core import ParameterCore  # type: ignore

# ** info: sidecards.artifacts imports
from src.sidecards.artifacts.path_provider import PathProvider  # type: ignore

__all__: list[str] = ["parameter_router"]

# ** info: building sidecards
_path_provider: PathProvider = PathProvider()

# ** info: building router
parameter_router: APIRouter = APIRouter(prefix=_path_provider.build_posix_path("parameter"), tags=["Parameters"])

# ** info: building router core
_parameter_core: ParameterCore = ParameterCore()


@parameter_router.post(
    description="search a prameter by its domain description",
    summary="search a prameter by its domain summary",
    path=_path_provider.build_posix_path("search"),
    response_model=ParameterSearchResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_search_parameter(parameter_search_request: ParameterSearchRequestDto = Body(...)) -> ParameterSearchResponseDto:
    parameter_search_response: ParameterSearchResponseDto = await _parameter_core.driver_search_parameter(parameter_search_request)
    return parameter_search_response
