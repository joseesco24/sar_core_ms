# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self

# ** info: health check dtos imports
from src.dtos.parameter_dtos import ParameterSearchResponseDto
from src.dtos.parameter_dtos import ParameterSearchRequestDto
from src.dtos.parameter_dtos import ParameterDataDto

__all__: list[str] = ["parameter_controller"]


class ParameterController:
    async def driver_parameter_search(self: Self, parameter_search_request: ParameterSearchRequestDto) -> ParameterSearchResponseDto:
        parameter_search_response: ParameterSearchResponseDto = ParameterSearchResponseDto()

        waste_1: ParameterDataDto = ParameterDataDto()
        waste_1.label = "waste 1"
        waste_1.value = 100

        waste_2: ParameterDataDto = ParameterDataDto()
        waste_2.label = "waste 2"
        waste_2.value = 100

        parameter_search_response.values = [waste_1, waste_2]

        return parameter_search_response


parameter_controller: ParameterController = ParameterController()
