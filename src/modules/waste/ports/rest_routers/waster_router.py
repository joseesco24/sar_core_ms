# !/usr/bin/python3

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: port dtos imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFilterByStatusRequestDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseListDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationRequestDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteUpdateStatusRequestDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClassifyRequestDto  # type: ignore

# ** info: app core imports
from src.modules.waste.cores.business.waste_core import WasteCore  # type: ignore

# ** info: sidecards.artifacts imports
from src.sidecards.artifacts.path_provider import PathProvider  # type: ignore

__all__: list[str] = ["waste_router"]

# ** info: building sidecards
_path_provider: PathProvider = PathProvider()

# ** info: building router
waste_router: APIRouter = APIRouter(prefix=_path_provider.build_posix_path("waste"), tags=["Wastes"])

# ** info: building router core
_waste_core: WasteCore = WasteCore()


@waste_router.post(
    description="allow to obtain the waste clasification according to its isotopes number, state of matter and weight in kg",
    summary="allow to obtain the waste clasification according to its isotopes number, state of matter and weight in kg",
    path=_path_provider.build_posix_path("clasification", "obtain"),
    response_model=WasteClasificationResponseDto,
    status_code=status.HTTP_200_OK,
)
async def _api_obtain_waste_classify(parameter_search_request: WasteClasificationRequestDto = Body(...)) -> WasteClasificationResponseDto:
    obtain_waste_classify_response: WasteClasificationResponseDto = await _waste_core.driver_obtain_waste_classify(parameter_search_request)
    return obtain_waste_classify_response


@waste_router.post(
    description="allow to change a waste store id, isotopes number and state of matter",
    summary="allow to change a waste store id, isotopes number and state of matter",
    path=_path_provider.build_posix_path("clasification", "update"),
    response_model=WasteFullDataResponseDto,
    status_code=status.HTTP_200_OK,
)
async def _api_update_waste_classify(waste_classify_request: WasteClassifyRequestDto = Body(...)) -> WasteFullDataResponseDto:
    update_waste_classify_response: WasteFullDataResponseDto = await _waste_core.driver_update_waste_classify(waste_classify_request)
    return update_waste_classify_response


@waste_router.post(
    description="allow to filter all the wastes by its status",
    summary="allow to filter all the wastes by its status",
    path=_path_provider.build_posix_path("status", "search"),
    response_model=WasteFullDataResponseListDto,
    status_code=status.HTTP_200_OK,
)
async def _api_search_waste_by_status(filter_waste_by_status_request: WasteFilterByStatusRequestDto = Body(...)) -> WasteFullDataResponseListDto:
    filtered_wastes_response: WasteFullDataResponseListDto = await _waste_core.driver_search_waste_by_status(filter_waste_by_status_request)
    return filtered_wastes_response


@waste_router.post(
    description="allow to change the waste status",
    summary="allow to change the waste status",
    path=_path_provider.build_posix_path("status", "update"),
    response_model=WasteFullDataResponseDto,
    status_code=status.HTTP_200_OK,
)
async def _api_update_waste_status(waste_update_status_request: WasteUpdateStatusRequestDto = Body(...)) -> WasteFullDataResponseDto:
    waste_update_status_response: WasteFullDataResponseDto = await _waste_core.driver_update_waste_status(waste_update_status_request)
    return waste_update_status_response
