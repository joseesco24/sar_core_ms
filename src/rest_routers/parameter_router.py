# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: artifacts imports
from src.artifacts.path.generator import generator

# ** info: health check dtos imports
from src.dtos.parameter_dtos import ParameterSearchResponseDto
from src.dtos.parameter_dtos import ParameterSearchRequestDto

# ** info: rest controllers imports
from src.rest_controllers.parameter_controller import ParameterController

__all__: list[str] = ["ParameterRouter"]


class ParameterRouter:
    def __init__(self: Self):
        # ** info: building class router
        self.router: APIRouter = APIRouter(prefix=generator.build_posix_path("parameter"))

        # ** info: bulding router endpoints
        self.router.add_api_route(
            path=generator.build_posix_path("search"),
            response_model=ParameterSearchResponseDto,
            endpoint=self.api_parameter_search,
            status_code=status.HTTP_200_OK,
            methods=["POST"],
        )

        # ** info: building router controllers
        self.parameter_controller: ParameterController = ParameterController()

    async def api_parameter_search(self: Self, parameter_search_request: ParameterSearchRequestDto = Body(...)) -> ParameterSearchResponseDto:
        parameter_search_response: ParameterSearchResponseDto = await self.parameter_controller.driver_parameter_search(parameter_search_request)
        return parameter_search_response
