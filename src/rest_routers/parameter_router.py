# !/usr/bin/python3
# type: ignore

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: artifacts imports
from src.artifacts.path.generator import generator

# ** info: dtos imports
from src.dtos.parameter_dtos import ParameterDtos

ParameterSearchResponseDto = ParameterDtos.ParameterSearchResponseDto
ParameterSearchRequestDto = ParameterDtos.ParameterSearchRequestDto

# ** info: rest controllers imports
from src.rest_controllers.parameter_controller import ParameterController

__all__: list[str] = ["parameter_router"]

# ** info: building class router
parameter_router: APIRouter = APIRouter(prefix=generator.build_posix_path("parameter"), tags=["Parameters"])

# ** info: building router controllers
parameter_controller: ParameterController = ParameterController()


@parameter_router.post(
    description="search a prameter by its domain description",
    summary="search a prameter by its domain summary",
    path=generator.build_posix_path("search"),
    response_model=ParameterSearchResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_parameter_search(parameter_search_request: ParameterSearchRequestDto = Body(...)) -> ParameterSearchResponseDto:
    parameter_search_response: ParameterSearchResponseDto = await parameter_controller.driver_parameter_search(parameter_search_request)
    return parameter_search_response
