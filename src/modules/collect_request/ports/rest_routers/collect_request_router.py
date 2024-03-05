# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self

# ** info: fastapi imports
from fastapi import APIRouter
from fastapi import status
from fastapi import Body

# ** info: port dtos imports
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestCreateResponseDto
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestCreateRequestDto

# ** info: app core imports
from src.modules.collect_request.cores.business.collect_request_core import CollectRequestCore

# ** info: sidecards.artifacts imports
from src.sidecards.artifacts.path_provider import PathProvider

__all__: list[str] = ["CollectRequestRouter"]


class CollectRequestRouter:

    def __init__(self: Self):
        # ** info: building artifacts
        self._path_provider: PathProvider = PathProvider()
        # ** info: building needed cores
        self._collect_request_core: CollectRequestCore = CollectRequestCore()
        # ** info: building class router
        self.router: APIRouter = APIRouter(prefix=self._path_provider.build_posix_path("collect-request"), tags=["Collect Requests"])

        # ** info: bulding router endpoints
        self.router.add_api_route(
            description="create a new collect request description",
            summary="create a new collect request summary",
            path=self._path_provider.build_posix_path("create"),
            response_model=CollectRequestCreateResponseDto,
            status_code=status.HTTP_200_OK,
            endpoint=self._api_create_request,
            methods=["POST"],
        )

    async def _api_create_request(self: Self, request_create_request: CollectRequestCreateRequestDto = Body(...)) -> CollectRequestCreateResponseDto:
        request_create_response: CollectRequestCreateResponseDto = await self._collect_request_core.driver_create_request(request_create_request)
        return request_create_response
