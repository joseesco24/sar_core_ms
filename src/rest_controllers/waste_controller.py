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

    def _obtain_waste_clasification(self: Self, state_waste: str, weight_in_kg: int, isotopes_number: int) -> int:
        return self.brms_port.obtain_waste_clasification(state_waste=state_waste, weight_in_kg=weight_in_kg, isotopes_number=isotopes_number)

    def _map_waste_classify_response(self: Self, clasification: int) -> WasteClasificationResponseDto:
        return WasteClasificationResponseDto(activityType=clasification)
