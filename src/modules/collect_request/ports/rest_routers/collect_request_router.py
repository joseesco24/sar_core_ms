# !/usr/bin/python3
# type: ignore

# ** info: fastapi imports
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: port dtos imports
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFullDataResponseDto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFindByStatusReqDto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFindByStatusResDto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestCreateRequestDto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestModifyByIdReqDto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestIdDto

# ** info: app core imports
from src.modules.collect_request.cores.business.collect_request_core import CollectRequestCore

# ** info: sidecards.artifacts imports
from src.general_sidecards.artifacts.path_provider import PathProvider

__all__: list[str] = ["collect_request_router"]

# ** info: building sidecards
_path_provider: PathProvider = PathProvider()

# ** info: building router
collect_request_router: APIRouter = APIRouter(prefix=_path_provider.build_posix_path("collect-request"), tags=["Collect Requests"])

# ** info: building router core
_collect_request_core: CollectRequestCore = CollectRequestCore()


@collect_request_router.post(
    description="create a new collect request description",
    summary="create a new collect request summary",
    path=_path_provider.build_posix_path("create"),
    response_model=CollectRequestFullDataResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_create_request(request_create_request: CollectRequestCreateRequestDto = Body(...)) -> CollectRequestFullDataResponseDto:
    request_create_response: CollectRequestFullDataResponseDto = await _collect_request_core.driver_create_request(request_create_request)
    return request_create_response


@collect_request_router.post(
    description="find all the collect request by its process status",
    summary="find all the collect request by its process status",
    path=_path_provider.build_posix_path("status", "search"),
    response_model=CollectRequestFindByStatusResDto,
    status_code=status.HTTP_200_OK,
)
async def api_find_request_by_status(request_find_request_by_status: CollectRequestFindByStatusReqDto = Body(...)) -> CollectRequestFindByStatusResDto:
    request_create_response: CollectRequestFindByStatusResDto = await _collect_request_core.driver_find_request_by_status(request_find_request_by_status)
    return request_create_response


@collect_request_router.post(
    description="modify the collect request status by its id",
    summary="modify the collect request status by its id",
    path=_path_provider.build_posix_path("status", "update"),
    response_model=CollectRequestFullDataResponseDto,
    status_code=status.HTTP_200_OK,
    deprecated=True,
)
async def api_modify_request_by_id(request_modify_request_by_id: CollectRequestModifyByIdReqDto = Body(...)) -> CollectRequestFullDataResponseDto:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="api deprecated")
    request_create_response: CollectRequestFullDataResponseDto = await _collect_request_core.driver_modify_request_by_id(request_modify_request_by_id)
    return request_create_response


@collect_request_router.post(
    description="modify the collect request status by to finished by its id",
    summary="modify the collect request status by to finished by its id",
    path=_path_provider.build_posix_path("status", "update", "finished"),
    response_model=CollectRequestFullDataResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_set_collect_request_to_finished(collect_request_set_finished: CollectRequestIdDto = Body(...)) -> CollectRequestFullDataResponseDto:
    request_create_response: CollectRequestFullDataResponseDto = await _collect_request_core.driver_set_collect_request_to_finished(collect_request_set_finished)
    return request_create_response


@collect_request_router.post(
    description="modify the collect request status by to approved by its id",
    summary="modify the collect request status by to approved by its id",
    path=_path_provider.build_posix_path("status", "update", "approved"),
    response_model=CollectRequestFullDataResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_set_collect_request_to_approved(collect_request_set_finished: CollectRequestIdDto = Body(...)) -> CollectRequestFullDataResponseDto:
    request_create_response: CollectRequestFullDataResponseDto = await _collect_request_core.driver_set_collect_request_to_approved(collect_request_set_finished)
    return request_create_response


@collect_request_router.post(
    description="modify the collect request status by to rejected by its id",
    summary="modify the collect request status by to rejected by its id",
    path=_path_provider.build_posix_path("status", "update", "rejected"),
    response_model=CollectRequestFullDataResponseDto,
    status_code=status.HTTP_200_OK,
)
async def api_set_collect_request_to_rejected(collect_request_set_finished: CollectRequestIdDto = Body(...)) -> CollectRequestFullDataResponseDto:
    request_create_response: CollectRequestFullDataResponseDto = await _collect_request_core.driver_set_collect_request_to_rejected(collect_request_set_finished)
    return request_create_response
