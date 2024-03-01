# !/usr/bin/python3
# type: ignore

# ** info: typing imports
from typing import Self

# ** info: dtos imports
from src.dtos.waste_dtos import WasteDtos

WasteClasificationResponseDto = WasteDtos.WasteClasificationResponseDto
WasteClasificationRequestDto = WasteDtos.WasteClasificationRequestDto

# ** info: ports imports
from src.rest_ports.brms_port import BrmsPort

# ** info: python imports
import logging

# ** info: fastapi imports
from fastapi import HTTPException
from fastapi import status

# ** info: typing imports
from typing import List

# ** info: dtos imports
from src.dtos.waste_dtos import WasteRequestControllerDtos

WasteClassifyRequestDto = WasteRequestControllerDtos.WasteClassifyRequestDto
WasteClassifyResponseDto = WasteRequestControllerDtos.WasteClassifyResponseDto

# ** info: users entity
from src.entities.parameter_entity import Parameter

# ** info: providers imports
from src.database.waste_provider import WasteProvider
from src.database.parameter_provider import ParameterProvider

__all__: list[str] = ["WasteController"]


class WasteController:
    def __init__(self: Self):
        # ** info: building controller needed providers
        self.brms_port: BrmsPort = BrmsPort()

    async def driver_waste_classify(self: Self, parameter_search_request: WasteClasificationRequestDto) -> WasteClasificationResponseDto:
        clasification: int = self._obtain_waste_clasification(
            state_waste=parameter_search_request.stateWaste, weight_in_kg=parameter_search_request.weightInKg, isotopes_number=parameter_search_request.isotopesNumber
        )
        waste_classify_response: WasteClasificationResponseDto = self._map_waste_classify_response(clasification=clasification)
        return waste_classify_response

    def _obtain_waste_clasification(self: Self, state_waste: str, weight_in_kg: float, isotopes_number: float) -> int:
        return self.brms_port.obtain_waste_clasification(state_waste=state_waste, weight_in_kg=weight_in_kg, isotopes_number=isotopes_number)

    def _map_waste_classify_response(self: Self, clasification: int) -> WasteClasificationResponseDto:
        return WasteClasificationResponseDto(activityType=clasification)
        self.waste_provider: WasteProvider = WasteProvider()
        self.parameter_provider: ParameterProvider = ParameterProvider()

    async def driver_waste_classify_save(self: Self, waste_classify_request: WasteClassifyRequestDto) -> WasteClassifyResponseDto:
        await self._validate_wastes_state(waste_classify_request=waste_classify_request)
        code: int = await self._waste_classify_request(waste_classify_request=waste_classify_request)
        if code == 1:
            message: str = "Exitoso"
        else:
            message: str = "Fallido"
        waste_classify_response: WasteClassifyResponseDto = await self._map_classify_response(code=code, message=message)
        return waste_classify_response

    async def _validate_wastes_state(self: Self, waste_classify_request: WasteClassifyRequestDto) -> None:
        waste_states: List[Parameter] = self.parameter_provider.search_parameters_by_domain(domain=r"stateWaste")
        waste_state_ids: set(int) = set([waste_state.id for waste_state in waste_states])
        if waste_classify_request.stateWaste not in waste_state_ids:
            valid_state_waste: str = r",".join(str(s) for s in waste_state_ids)
            logging.error(f"state type {waste_classify_request.stateWaste} is not valid valid types are {valid_state_waste}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"state type {waste_classify_request.stateWaste} is not valid")

    async def _waste_classify_request(self: Self, waste_classify_request: WasteClassifyRequestDto) -> int:
        code: int = self.waste_provider.classify_waste(
            uuid=waste_classify_request.wasteId,
            isotopes_number=waste_classify_request.isotopesNumber,
            state_waste=waste_classify_request.stateWaste,
            store=waste_classify_request.storeId,
        )
        return code

    async def _map_classify_response(self: Self, code: int, message: str) -> WasteClassifyResponseDto:
        return WasteClassifyResponseDto(code=code, message=message)


# ** info: editar esto al trabajar la tajada de los residuos
