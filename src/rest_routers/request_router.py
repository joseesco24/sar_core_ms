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
from src.dtos.request_dtos import RequestCreateResponseDto
from src.dtos.request_dtos import RequestCreateRequestDto

# ** info: rest controllers imports
from src.rest_controllers.request_controller import RequestController

__all__: list[str] = ["RequestRouter"]


class RequestRouter:
    def __init__(self: Self):
        # ** info: building class router
        self.router: APIRouter = APIRouter(prefix=generator.build_posix_path("request"))

        # ** info: bulding router endpoints
        self.router.add_api_route(
            path=generator.build_posix_path("create"),
            response_model=RequestCreateResponseDto,
            endpoint=self.api_request_create,
            status_code=status.HTTP_200_OK,
            methods=["POST"],
        )

        # ** info: building router controllers
        self.request_controller: RequestController = RequestController()

    async def api_request_create(self: Self, request_create_request: RequestCreateRequestDto = Body(...)) -> RequestCreateResponseDto:
        request_create_response: RequestCreateResponseDto = await self.request_controller.driver_request_create(request_create_request)
        return request_create_response
