# !/usr/bin/python3
# type: ignore

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: dtos imports
from src.modules.waste.dtos.waste_dtos import WasteRequestControllerDtos
from src.modules.waste.dtos.waste_dtos import WasteDtos

WasteClassifyResponseDto = WasteRequestControllerDtos.WasteClassifyResponseDto
WasteClassifyRequestDto = WasteRequestControllerDtos.WasteClassifyRequestDto
WasteClasificationResponseDto = WasteDtos.WasteClasificationResponseDto
WasteClasificationRequestDto = WasteDtos.WasteClasificationRequestDto

# ** info: rest controllers imports
from src.modules.waste.cores.waste_core import WasteCore

# ** info: artifacts imports
from src.sidecards.path.generator import generator

__all__: list[str] = ["waste_router"]

# ** info: building class router
waste_router: APIRouter = APIRouter(prefix=generator.build_posix_path("waste"), tags=["Wastes"])

# ** info: building router controllers
waste_core: WasteCore = WasteCore()


@waste_router.post(
    description="classifies the waste according to its attributes",
    summary="classifies the waste according to its attributes",
    path=generator.build_posix_path("clasification", "obtain"),
    response_model=WasteClasificationResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_obtain_waste_classify(parameter_search_request: WasteClasificationRequestDto = Body(...)) -> WasteClasificationResponseDto:
    waste_classify_response: WasteClasificationResponseDto = await waste_core.driver_obtain_waste_classify(parameter_search_request)
    return waste_classify_response


@waste_router.post(
    description="classify a waste by id request description",
    summary="classify a waste by id request summary",
    path=generator.build_posix_path("clasification", "update"),
    response_model=WasteClassifyResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_update_waste_classify(waste_classify_request: WasteClassifyRequestDto = Body(...)) -> WasteClassifyResponseDto:
    waste_classify_response: WasteClassifyResponseDto = await waste_core.driver_update_waste_classify(waste_classify_request)
    return waste_classify_response
