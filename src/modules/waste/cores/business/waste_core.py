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

# ** info: cores imports
from src.modules.parameter.cores.business.parameter_core import ParameterCore  # type: ignore

# ** info: dtos imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFilterByStatusRequestDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationRequestDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseListDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteUpdateStatusRequestDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClassifyRequestDto  # type: ignore

# ** info: entities imports
from src.modules.waste.adapters.database_providers_entities.waste_entity import Waste  # type: ignore

# ** info: providers imports
from src.modules.waste.adapters.database_providers.waste_provider import WasteProvider  # type: ignore

# ** info: ports imports
from src.modules.waste.adapters.rest_services.brms_service import BrmsService  # type: ignore

# ** info: sidecards.artifacts imports
from src.sidecards.artifacts.datetime_provider import DatetimeProvider  # type: ignore

__all__: list[str] = ["WasteCore"]


class WasteCore:

    # !------------------------------------------------------------------------
    # ! info: core atributtes and constructor section start
    # !------------------------------------------------------------------------

    def __init__(self: Self):
        # ** info: cores building
        self._parameter_core: ParameterCore = ParameterCore()
        # ** info: providers building
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
        obtain_waste_classify_response: WasteClasificationResponseDto = await self._map_waste_classify_response(clasification=clasification)
        logging.info("driver_obtain_waste_classify ended")
        return obtain_waste_classify_response

    async def driver_update_waste_classify(self: Self, waste_classify_request: WasteClassifyRequestDto) -> WasteFullDataResponseDto:
        logging.info("starting driver_update_waste_classify")
        await self._validate_wastes_state(waste_classify_request=waste_classify_request)
        waste_info: Waste = await self._waste_classify_request(waste_classify_request=waste_classify_request)
        update_waste_classify_response: WasteFullDataResponseDto = await self._map_full_data_response(waste_info=waste_info)
        logging.info("driver_update_waste_classify ended")
        return update_waste_classify_response

    async def driver_search_waste_by_status(self: Self, filter_waste_by_status_request: WasteFilterByStatusRequestDto) -> WasteFullDataResponseListDto:
        logging.info("starting driver_search_waste_by_status")
        await self._validate_waste_process_status(process_status=filter_waste_by_status_request.processStatus)
        wastes_info: List[Waste] = self._waste_provider.list_wastes_by_process_status(process_status=filter_waste_by_status_request.processStatus)
        filtered_wastes_response: WasteFullDataResponseListDto = await self._map_full_data_response_list(wastes_info=wastes_info)
        logging.info("driver_search_waste_by_status ended")
        return filtered_wastes_response

    async def driver_update_waste_status(self: Self, waste_update_status_request: WasteUpdateStatusRequestDto) -> WasteFullDataResponseDto:
        logging.info("starting driver_update_waste_status")
        await self._validate_waste_process_status(process_status=waste_update_status_request.processStatus)
        waste_info: Waste = self._waste_provider.update_waste_status(uuid=waste_update_status_request.wasteId, process_status=waste_update_status_request.processStatus)
        waste_update_status_response: WasteFullDataResponseDto = await self._map_full_data_response(waste_info=waste_info)
        logging.info("driver_update_waste_status ended")
        return waste_update_status_response

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
        waste_state_ids: Set[int] = await self._parameter_core.cf_get_set_of_parameter_ids_by_domain(domain=r"wasteProcessStatus")
        if process_status not in waste_state_ids:
            valid_state_waste: str = r",".join(str(s) for s in waste_state_ids)
            logging.error(f"process status {process_status} is not valid valid types are {valid_state_waste}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"process status {process_status} is not valid")

    async def _validate_wastes_state(self: Self, waste_classify_request: WasteClassifyRequestDto) -> None:
        waste_state_ids: Set[int] = await self._parameter_core.cf_get_set_of_parameter_ids_by_domain(domain=r"stateWaste")
        if waste_classify_request.stateWaste not in waste_state_ids:
            valid_state_waste: str = r",".join(str(s) for s in waste_state_ids)
            logging.error(f"state type {waste_classify_request.stateWaste} is not valid valid types are {valid_state_waste}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"state type {waste_classify_request.stateWaste} is not valid")

    async def _waste_classify_request(self: Self, waste_classify_request: WasteClassifyRequestDto) -> Waste:
        waste_info: Waste = self._waste_provider.update_waste_internal_classification_info(
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
            weightInKg=float(waste_info.weight_in_kg),
            volumeInL=float(waste_info.volume_in_l),
            processStatus=waste_info.process_status,
            description=waste_info.description,
            requestId=waste_info.request_uuid,
            packaging=waste_info.packaging,
            type=waste_info.type,
            note=waste_info.note,
            id=waste_info.uuid,
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
