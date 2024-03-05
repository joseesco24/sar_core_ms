# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: port dtos imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationResponseDto
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFilterByStatusRequestDto
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseListDto
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationRequestDto
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteUpdateStatusRequestDto
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseDto
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClassifyRequestDto

# ** info: app core imports
from src.modules.waste.cores.business.waste_core import WasteCore

# ** info: sidecards imports
from src.sidecards.artifacts.path_provider import PathProvider

__all__: list[str] = ["WasteRouter"]


class WasteRouter:

    def __init__(self: Self):
        # ** info: building artifacts
        self._path_provider: PathProvider = PathProvider()
        # ** info: building needed cores
        self._waste_core: WasteCore = WasteCore()
        # ** info: building class router
        self.router: APIRouter = APIRouter(prefix=self._path_provider.build_posix_path("waste"), tags=["Wastes"])

        self.router.add_api_route(
            description="allow to obtain the waste clasification according to its isotopes number, state of matter and weight in kg",
            summary="allow to obtain the waste clasification according to its isotopes number, state of matter and weight in kg",
            path=self._path_provider.build_posix_path("clasification", "obtain"),
            response_model=WasteClasificationResponseDto,
            status_code=status.HTTP_200_OK,
            endpoint=self._api_obtain_waste_classify,
            methods=["POST"],
        )

        self.router.add_api_route(
            description="allow to change a waste store id, isotopes number and state of matter",
            summary="allow to change a waste store id, isotopes number and state of matter",
            path=self._path_provider.build_posix_path("clasification", "update"),
            response_model=WasteFullDataResponseDto,
            status_code=status.HTTP_200_OK,
            endpoint=self._api_update_waste_classify,
            methods=["POST"],
        )

        self.router.add_api_route(
            description="allow to filter all the wastes by its status",
            summary="allow to filter all the wastes by its status",
            path=self._path_provider.build_posix_path("status", "search"),
            response_model=WasteFullDataResponseListDto,
            status_code=status.HTTP_200_OK,
            endpoint=self._api_search_waste_by_status,
            methods=["POST"],
        )

        self.router.add_api_route(
            description="allow to change the waste status",
            summary="allow to change the waste status",
            path=self._path_provider.build_posix_path("status", "update"),
            response_model=WasteFullDataResponseDto,
            status_code=status.HTTP_200_OK,
            endpoint=self._api_update_waste_status,
            methods=["POST"],
        )

    async def _api_obtain_waste_classify(self: Self, parameter_search_request: WasteClasificationRequestDto = Body(...)) -> WasteClasificationResponseDto:
        obtain_waste_classify_response: WasteClasificationResponseDto = await self._waste_core.driver_obtain_waste_classify(parameter_search_request)
        return obtain_waste_classify_response

    async def _api_update_waste_classify(self: Self, waste_classify_request: WasteClassifyRequestDto = Body(...)) -> WasteFullDataResponseDto:
        update_waste_classify_response: WasteFullDataResponseDto = await self._waste_core.driver_update_waste_classify(waste_classify_request)
        return update_waste_classify_response

    async def _api_search_waste_by_status(self: Self, filter_waste_by_status_request: WasteFilterByStatusRequestDto = Body(...)) -> WasteFullDataResponseListDto:
        filtered_wastes_response: WasteFullDataResponseListDto = await self._waste_core.driver_search_waste_by_status(filter_waste_by_status_request)
        return filtered_wastes_response

    async def _api_update_waste_status(self: Self, waste_update_status_request: WasteUpdateStatusRequestDto = Body(...)) -> WasteFullDataResponseDto:
        waste_update_status_response: WasteFullDataResponseDto = await self._waste_core.driver_update_waste_status(waste_update_status_request)
        return waste_update_status_response
