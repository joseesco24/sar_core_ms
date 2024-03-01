# !/usr/bin/python3
# type: ignore

# ** info: python imports
import logging

# ** info: typing imports
from typing import Self
from typing import List

# ** info: dtos imports
from src.dtos.parameter_dtos import ParameterDtos

ParameterSearchResponseDto = ParameterDtos.ParameterSearchResponseDto
ParameterSearchRequestDto = ParameterDtos.ParameterSearchRequestDto
ParameterDataDto = ParameterDtos.ParameterDataDto

# ** info: entities imports
from src.entities.parameter_entity import Parameter

# ** info: providers imports
from src.database.parameter_provider import ParameterProvider

__all__: list[str] = ["ParameterCore"]


class ParameterCore:

    # !------------------------------------------------------------------------
    # ! info: core atributtes and constructor section start
    # !------------------------------------------------------------------------

    def __init__(self: Self):
        # ** info: providers building
        self.parameter_provider: ParameterProvider = ParameterProvider()

    # !------------------------------------------------------------------------
    # ! info: driver methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from the routers layer
    # ! warning: a method only can be declared in this section if it is going to be called from the routers layer
    # !------------------------------------------------------------------------

    async def driver_search_parameter(self: Self, parameter_search_request: ParameterSearchRequestDto) -> ParameterSearchResponseDto:
        logging.info("starting driver_search_parameter")
        parameters: List[Parameter] = await self._search_by_domain(domain=parameter_search_request.domain)
        parameter_search_response: ParameterSearchResponseDto = await self._map_parameter_response(parameters=parameters)
        logging.info("driver_search_parameter ended")
        return parameter_search_response

    # !------------------------------------------------------------------------
    # ! info: core methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from another core or from a driver method
    # ! warning: a method only can be declared in this section if it is going to be called from another core or from a driver method
    # !------------------------------------------------------------------------

    # !------------------------------------------------------------------------
    # ! info: private class methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from inside this core
    # ! warning: a method only can be declared in this section if it is going to be called from inside this core
    # !------------------------------------------------------------------------

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
