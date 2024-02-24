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
from src.dtos.collect_request_dtos import CollectRequestCreateResponseDto
from src.dtos.collect_request_dtos import CollectRequestCreateRequestDto

# ** info: rest controllers imports
from src.rest_controllers.collect_request_controller import CollectRequestController

__all__: list[str] = ["CollectRequestRouter"]


class CollectRequestRouter:
    def __init__(self: Self):
        # ** info: building class router
        self.router: APIRouter = APIRouter(prefix=generator.build_posix_path("request"))

        # ** info: bulding router endpoints
        self.router.add_api_route(
            path=generator.build_posix_path("create"),
            response_model=CollectRequestCreateResponseDto,
            endpoint=self.api_request_create,
            status_code=status.HTTP_200_OK,
            methods=["POST"],
        )

        # ** info: building router controllers
        self.collect_request_controller: CollectRequestController = CollectRequestController()

    async def api_request_create(self: Self, request_create_request: CollectRequestCreateRequestDto = Body(...)) -> CollectRequestCreateResponseDto:
        request_create_response: CollectRequestCreateResponseDto = await self.collect_request_controller.driver_request_create(request_create_request)
        return request_create_response
