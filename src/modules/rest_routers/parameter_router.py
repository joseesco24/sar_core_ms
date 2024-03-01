# !/usr/bin/python3
# type: ignore

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: dtos imports
from src.modules.dtos.parameter_dtos import ParameterDtos

ParameterSearchResponseDto = ParameterDtos.ParameterSearchResponseDto
ParameterSearchRequestDto = ParameterDtos.ParameterSearchRequestDto

# ** info: rest controllers imports
from src.modules.core.parameter_core import ParameterCore

# ** info: artifacts imports
from src.sidecards.path.generator import generator

__all__: list[str] = ["parameter_router"]

# ** info: building class router
parameter_router: APIRouter = APIRouter(prefix=generator.build_posix_path("parameter"), tags=["Parameters"])

# ** info: building router controllers
parameter_core: ParameterCore = ParameterCore()


@parameter_router.post(
    description="search a prameter by its domain description",
    summary="search a prameter by its domain summary",
    path=generator.build_posix_path("search"),
    response_model=ParameterSearchResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_search_parameter(parameter_search_request: ParameterSearchRequestDto = Body(...)) -> ParameterSearchResponseDto:
    parameter_search_response: ParameterSearchResponseDto = await parameter_core.driver_search_parameter(parameter_search_request)
    return parameter_search_response
