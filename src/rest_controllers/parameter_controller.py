# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self
from typing import List

# ** info: health check dtos imports
from src.dtos.parameter_dtos import ParameterSearchResponseDto
from src.dtos.parameter_dtos import ParameterSearchRequestDto
from src.dtos.parameter_dtos import ParameterDataDto

# ** info: providers imports
from src.database.parameter_provider import ParameterProvider

# ** info: users entity
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
        parameter_search_response: ParameterSearchResponseDto = ParameterSearchResponseDto()
        parameter_search_response.values = await self._map_parameters_data(parameters=parameters)
        return parameter_search_response

    async def _map_parameters_data(self: Self, parameters: List[Parameter]) -> List[ParameterDataDto]:
        parameters_data: List[ParameterDataDto] = []
        for parameter in parameters:
            parameter_data: ParameterDataDto = await self._map_parameter_data(parameter=parameter)
            parameters_data.append(parameter_data)
        return parameters_data

    async def _map_parameter_data(self: Self, parameter: Parameter) -> ParameterDataDto:
        parameter_data: ParameterDataDto = ParameterDataDto()
        parameter_data.label = parameter.value
        parameter_data.value = parameter.id
        return parameter_data
