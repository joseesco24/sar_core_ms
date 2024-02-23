# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self

# ** info: health check dtos imports
from src.dtos.collect_request_dtos import CollectRequestCreateResponseDto
from src.dtos.collect_request_dtos import CollectRequestCreateRequestDto
from src.dtos.collect_request_dtos import ResponseRequestDataDto
from src.dtos.collect_request_dtos import ResponseWasteDataDto

__all__: list[str] = ["CollectRequestController"]


class CollectRequestController:
    async def driver_request_create(self: Self, request_create_request: CollectRequestCreateRequestDto) -> CollectRequestCreateResponseDto:
        request_create_response: CollectRequestCreateResponseDto = CollectRequestCreateResponseDto()

        request_detail: ResponseRequestDataDto = ResponseRequestDataDto()
        request_detail.id = "ee8a7b81-9062-45e1-9a31-ea9989571719"
        request_detail.productionCenterId = 123456789
        request_detail.collectDate = "2021-01-01"

        waste_detail: ResponseWasteDataDto = ResponseWasteDataDto()
        waste_detail.requestId = "ee8a7b81-9062-45e1-9a31-ea9989571719"
        waste_detail.id = "16f40643-e560-4831-b584-5571fd11fefd"
        waste_detail.description = "waste description"
        waste_detail.note = "waste note details"
        waste_detail.weightInKg = 100.12
        waste_detail.volumeInL = 200.24
        waste_detail.packaging = 1
        waste_detail.type = 1

        request_create_response.request = request_detail
        request_create_response.waste = [waste_detail]

        return request_create_response
