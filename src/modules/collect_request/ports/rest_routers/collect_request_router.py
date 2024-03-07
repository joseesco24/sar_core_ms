# !/usr/bin/python3
# type: ignore

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: port dtos imports
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestCreateResponseDto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestCreateRequestDto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFindByStatusReqDto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFindByStatusResDto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestModifyByIdReqDto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import ResponseRequestDataDto

# ** info: app core imports
from src.modules.collect_request.cores.business.collect_request_core import CollectRequestCore

# ** info: sidecards.artifacts imports
from src.sidecards.artifacts.path_provider import PathProvider

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
    response_model=CollectRequestCreateResponseDto,
    status_code=status.HTTP_200_OK,
)
async def _api_create_request(request_create_request: CollectRequestCreateRequestDto = Body(...)) -> CollectRequestCreateResponseDto:
    request_create_response: CollectRequestCreateResponseDto = await _collect_request_core.driver_create_request(request_create_request)
    return request_create_response


@collect_request_router.post(
    description="find all the collect request by its process status",
    summary="find all the collect request by its process status",
    path=_path_provider.build_posix_path("status", "search"),
    response_model=CollectRequestFindByStatusResDto,
    status_code=status.HTTP_200_OK,
)
async def _api_find_collectReq_by_status(request_find_request_by_status: CollectRequestFindByStatusReqDto = Body(...)) -> CollectRequestFindByStatusResDto:
    request_create_response: CollectRequestFindByStatusResDto = await _collect_request_core.driver_find_request_by_status(request_find_request_by_status)
    return request_create_response


@collect_request_router.post(
    description="modify the collect request status by its id",
    summary="modify the collect request status by its id",
    path=_path_provider.build_posix_path("status", "update"),
    response_model=ResponseRequestDataDto,
    status_code=status.HTTP_200_OK,
)
async def _api_modify_collectReq_by_id(request_modify_request_by_id: CollectRequestModifyByIdReqDto = Body(...)) -> ResponseRequestDataDto:
    request_create_response: ResponseRequestDataDto = await _collect_request_core.driver_modify_request_by_id(request_modify_request_by_id)
    return request_create_response
