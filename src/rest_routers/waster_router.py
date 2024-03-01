# !/usr/bin/python3
# type: ignore

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: artifacts imports
from src.artifacts.path.generator import generator

# ** info: dtos imports
from src.dtos.waste_dtos import WasteDtos

WasteClasificationResponseDto = WasteDtos.WasteClasificationResponseDto
WasteClasificationRequestDto = WasteDtos.WasteClasificationRequestDto
from src.dtos.waste_dtos import WasteRequestControllerDtos

WasteClassifyResponseDto = WasteRequestControllerDtos.WasteClassifyResponseDto
WasteClassifyRequestDto = WasteRequestControllerDtos.WasteClassifyRequestDto

# ** info: rest controllers imports
from src.rest_controllers.waste_controller import WasteController

__all__: list[str] = ["waste_router"]

# ** info: building class router
waste_router: APIRouter = APIRouter(prefix=generator.build_posix_path("waste"), tags=["Waste"])
waste_router: APIRouter = APIRouter(prefix=generator.build_posix_path("waste"), tags=["Wastes"])

# ** info: building router controllers
waste_controller: WasteController = WasteController()


@waste_router.post(
    description="classifies the waste according to its attributes",
    summary="classifies the waste according to its attributes",
    path=generator.build_posix_path("clasification"),
    response_model=WasteClasificationResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_waste_classify(parameter_search_request: WasteClasificationRequestDto = Body(...)) -> WasteClasificationResponseDto:
    waste_classify_response: WasteClasificationResponseDto = await waste_controller.driver_waste_classify(parameter_search_request)
    return waste_classify_response


@waste_router.post(
    description="classify a waste by id request description",
    summary="classify a waste by id request summary",
    path=generator.build_posix_path("classify"),
    response_model=WasteClassifyResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_waste_classify_save(waste_classify_request: WasteClassifyRequestDto = Body(...)) -> WasteClassifyResponseDto:
    waste_classify_response: WasteClassifyResponseDto = await waste_controller.driver_waste_classify_save(waste_classify_request)
    return waste_classify_response
