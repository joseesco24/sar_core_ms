# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self
from typing import List

# ** info: dtos imports
from src.dtos.parameter_dtos import ParameterDtos

ParameterSearchResponseDto = ParameterDtos.ParameterSearchResponseDto
ParameterSearchRequestDto = ParameterDtos.ParameterSearchRequestDto
ParameterDataDto = ParameterDtos.ParameterDataDto

# ** info: providers imports
from src.database.parameter_provider import ParameterProvider

# ** info: entities imports
from src.entities.parameter_entity import Parameter

__all__: list[str] = ["ParameterController"]


class ParameterController:
    def __init__(self: Self):
        # ** info: building controller needed providers
        self.parameter_provider: ParameterProvider = ParameterProvider()

    async def driver_parameter_search(self: Self, parameter_search_request: ParameterSearchRequestDto) -> ParameterSearchResponseDto:
        parameters: List[Parameter] = await self._search_by_domain(domain=parameter_search_request.domain)
        parameter_search_response: ParameterSearchResponseDto = await self._map_parameter_response(parameters=parameters)
        return parameter_search_response

    async def _search_by_domain(self: Self, domain: str) -> Parameter:
        parameters: List[Parameter] = self.parameter_provider.search_parameters_by_domain(domain=domain)
        return parameters

    async def _map_parameter_response(self: Self, parameters: List[Parameter]) -> ParameterSearchResponseDto:
        return ParameterSearchResponseDto(values=await self._map_parameters_data(parameters=parameters))

    async def _map_parameters_data(self: Self, parameters: List[Parameter]) -> List[ParameterDataDto]:
        parameters_data: List[ParameterDataDto] = []
        for parameter in parameters:
            parameter_data: ParameterDataDto = await self._map_parameter_data(parameter=parameter)
            parameters_data.append(parameter_data)
        return parameters_data

    async def _map_parameter_data(self: Self, parameter: Parameter) -> ParameterDataDto:
        return ParameterDataDto(label=parameter.value, value=parameter.id)
