# !/usr/bin/python3
# type: ignore

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: artifacts imports
from src.artifacts.path.generator import generator

# ** info: dtos imports
from src.dtos.collect_request_dtos import CollectRequestControllerDtos

CollectRequestCreateResponseDto = CollectRequestControllerDtos.CollectRequestCreateResponseDto
CollectRequestCreateRequestDto = CollectRequestControllerDtos.CollectRequestCreateRequestDto

# ** info: rest controllers imports
from src.rest_controllers.collect_request_controller import CollectRequestController

__all__: list[str] = ["collect_request_router"]

# ** info: building class router
collect_request_router: APIRouter = APIRouter(prefix=generator.build_posix_path("request"), tags=["Collect Requests"])

# ** info: building router controllers
collect_request_controller: CollectRequestController = CollectRequestController()


@collect_request_router.post(
    description="create a new collect request description",
    summary="create a new collect request summary",
    path=generator.build_posix_path("create"),
    response_model=CollectRequestCreateResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_request_create(request_create_request: CollectRequestCreateRequestDto = Body(...)) -> CollectRequestCreateResponseDto:
    request_create_response: CollectRequestCreateResponseDto = await collect_request_controller.driver_request_create(request_create_request)
    return request_create_response
