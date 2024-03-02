# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: port dtos imports
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos import ParameterSearchResponseDto
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos import ParameterSearchRequestDto

# ** info: app core imports
from src.modules.parameter.cores.business.parameter_core import ParameterCore

# ** info: sidecards imports
from src.sidecards.artifacts.path_provider import PathProvider

__all__: list[str] = ["ParameterRouter"]


class ParameterRouter:

    def __init__(self: Self):
        # ** info: building artifacts
        self._path_provider: PathProvider = PathProvider()
        # ** info: building needed cores
        self._parameter_core: ParameterCore = ParameterCore()
        # ** info: building class router
        self.router: APIRouter = APIRouter(prefix=self._path_provider.build_posix_path("parameter"), tags=["Parameters"])

        # ** info: bulding router endpoints
        self.router.add_api_route(
            description="search a prameter by its domain description",
            summary="search a prameter by its domain summary",
            path=self._path_provider.build_posix_path("search"),
            response_model=ParameterSearchResponseDto,
            status_code=status.HTTP_200_OK,
            endpoint=self._api_search_parameter,
            methods=["POST"],
        )

    async def _api_search_parameter(self: Self, parameter_search_request: ParameterSearchRequestDto = Body(...)) -> ParameterSearchResponseDto:
        parameter_search_response: ParameterSearchResponseDto = await self._parameter_core.driver_search_parameter(parameter_search_request)
        return parameter_search_response
