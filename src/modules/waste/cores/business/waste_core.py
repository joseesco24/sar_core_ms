# !/usr/bin/python3

# ** info: python imports
import logging

# ** info: typing imports
from typing import List
from typing import Self
from typing import Set

# ** info: fastapi imports
from fastapi import HTTPException
from fastapi import status

# ** info: dtos imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFilterByStatusRequestDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationRequestDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseListDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClassifyRequestDto  # type: ignore

# ** info: entities imports
from src.modules.parameter.adapters.database_providers_entities.parameter_entity import Parameter  # type: ignore
from src.modules.waste.adapters.database_providers_entities.waste_entity import Waste  # type: ignore

# ** info: providers imports
from src.modules.parameter.adapters.database_providers.parameter_provider import ParameterProvider  # type: ignore
from src.modules.waste.adapters.database_providers.waste_provider import WasteProvider  # type: ignore

# ** info: ports imports
from src.modules.waste.adapters.rest_services.brms_service import BrmsService  # type: ignore

# ** info: sidecards imports
from src.sidecards.artifacts.datetime_provider import DatetimeProvider  # type: ignore


__all__: list[str] = ["WasteCore"]


class WasteCore:

    # !------------------------------------------------------------------------
    # ! info: core atributtes and constructor section start
    # !------------------------------------------------------------------------

    def __init__(self: Self):
        # ** info: providers building
        self._parameter_provider: ParameterProvider = ParameterProvider()
        self._waste_provider: WasteProvider = WasteProvider()
        # ** info: rest services building
        self._brms_service: BrmsService = BrmsService()
        # ** info: sidecards building
        self._datetime_provider: DatetimeProvider = DatetimeProvider()

    # !------------------------------------------------------------------------
    # ! info: driver methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from the routers layer
    # ! warning: a method only can be declared in this section if it is going to be called from the routers layer
    # !------------------------------------------------------------------------

    async def driver_obtain_waste_classify(self: Self, parameter_search_request: WasteClasificationRequestDto) -> WasteClasificationResponseDto:
        logging.info("starting driver_obtain_waste_classify")
        clasification: int = await self._obtain_waste_clasification(
            state_waste=parameter_search_request.stateWaste, weight_in_kg=parameter_search_request.weightInKg, isotopes_number=parameter_search_request.isotopesNumber
        )
        waste_classify_response: WasteClasificationResponseDto = await self._map_waste_classify_response(clasification=clasification)
        logging.info("driver_obtain_waste_classify ended")
        return waste_classify_response

    async def driver_update_waste_classify(self: Self, waste_classify_request: WasteClassifyRequestDto) -> WasteFullDataResponseDto:
        logging.info("starting driver_update_waste_classify")
        await self._validate_wastes_state(waste_classify_request=waste_classify_request)
        waste_info: Waste = await self._waste_classify_request(waste_classify_request=waste_classify_request)
        waste_classify_response: WasteFullDataResponseDto = await self._map_full_data_response(waste_info=waste_info)
        logging.info("driver_update_waste_classify ended")
        return waste_classify_response

    async def driver_filter_waste_by_status(self: Self, filter_waste_by_status_request: WasteFilterByStatusRequestDto) -> WasteFullDataResponseListDto:
        logging.info("starting driver_update_waste_classify")
        await self._validate_waste_process_status(process_status=filter_waste_by_status_request.processStatus)
        wastes_info: List[Waste] = self._waste_provider.serch_wastes_by_process_status(process_status=filter_waste_by_status_request.processStatus)
        waste_classify_response: WasteFullDataResponseListDto = await self._map_full_data_response_list(wastes_info=wastes_info)
        logging.info("driver_update_waste_classify ended")
        return waste_classify_response

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

    async def _obtain_waste_clasification(self: Self, state_waste: str, weight_in_kg: float, isotopes_number: float) -> int:
        return self._brms_service.obtain_waste_clasification(state_waste=state_waste, weight_in_kg=weight_in_kg, isotopes_number=isotopes_number)

    async def _map_waste_classify_response(self: Self, clasification: int) -> WasteClasificationResponseDto:
        return WasteClasificationResponseDto(storeType=clasification)

    async def _validate_waste_process_status(self: Self, process_status: int) -> None:
        waste_states: List[Parameter] = self._parameter_provider.search_parameters_by_domain(domain=r"wasteProcessStatus")
        waste_state_ids: Set[int] = set([waste_state.id for waste_state in waste_states])
        if process_status not in waste_state_ids:
            valid_state_waste: str = r",".join(str(s) for s in waste_state_ids)
            logging.error(f"process status {process_status} is not valid valid types are {valid_state_waste}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"process status {process_status} is not valid")

    async def _validate_wastes_state(self: Self, waste_classify_request: WasteClassifyRequestDto) -> None:
        waste_states: List[Parameter] = self._parameter_provider.search_parameters_by_domain(domain=r"stateWaste")
        waste_state_ids: Set[int] = set([waste_state.id for waste_state in waste_states])
        if waste_classify_request.stateWaste not in waste_state_ids:
            valid_state_waste: str = r",".join(str(s) for s in waste_state_ids)
            logging.error(f"state type {waste_classify_request.stateWaste} is not valid valid types are {valid_state_waste}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"state type {waste_classify_request.stateWaste} is not valid")

    async def _waste_classify_request(self: Self, waste_classify_request: WasteClassifyRequestDto) -> Waste:
        waste_info: Waste = self._waste_provider.classify_waste(
            uuid=waste_classify_request.wasteId,
            isotopes_number=waste_classify_request.isotopesNumber,
            state_waste=waste_classify_request.stateWaste,
            store=waste_classify_request.storeId,
        )
        return waste_info

    async def _map_full_data_response_list(self: Self, wastes_info: List[Waste]) -> WasteFullDataResponseListDto:
        return WasteFullDataResponseListDto(values=await self._map_full_data_responses(wastes_info=wastes_info))

    async def _map_full_data_responses(self: Self, wastes_info: List[Waste]) -> List[WasteFullDataResponseDto]:
        return [await self._map_full_data_response(waste_info=waste_info) for waste_info in wastes_info]

    async def _map_full_data_response(self: Self, waste_info: Waste) -> WasteFullDataResponseDto:

        created: str = self._datetime_provider.prettify_date_time_obj(date_time_obj=waste_info.create)
        updated: str = self._datetime_provider.prettify_date_time_obj(date_time_obj=waste_info.update)

        waste_full_data_response: WasteFullDataResponseDto = WasteFullDataResponseDto(
            id=waste_info.uuid,
            requestId=waste_info.request_uuid,
            type=waste_info.type,
            packaging=waste_info.packaging,
            processStatus=waste_info.process_status,
            weightInKg=float(waste_info.weight_in_kg),
            volumeInL=float(waste_info.volume_in_l),
            description=waste_info.description,
            note=waste_info.note,
            create=created,
            update=updated,
        )

        if waste_info.isotopes_number is not None:
            waste_full_data_response.isotopesNumber = float(waste_info.isotopes_number)

        if waste_info.state_waste is not None:
            waste_full_data_response.stateWaste = waste_info.state_waste

        if waste_info.store is not None:
            waste_full_data_response.storeType = waste_info.store

        return waste_full_data_response
