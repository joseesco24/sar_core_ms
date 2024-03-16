# !/usr/bin/python3

# ** info: python imports
import logging

# ** info: asyncio imports
from functools import reduce
from asyncio import gather

# ** info: typing imports
from typing import Union
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

# ** info: adapter imports
from src.modules.waste.adapters.rest_services.warehouse_ms_service import WarehouseMsService  # type: ignore
from src.modules.waste.adapters.rest_services.brms_service import BrmsService  # type: ignore

# ** info: sidecards.artifacts imports
from src.general_sidecards.artifacts.datetime_provider import DatetimeProvider  # type: ignore

# ** info: cachetools imports
from cachetools import TTLCache  # type: ignore

# ** info: asyncache imports
from asyncache import cached as async_cached  # type: ignore

__all__: list[str] = ["WasteCore"]


class WasteCore:

    # !------------------------------------------------------------------------
    # ! info: core slots section start
    # !------------------------------------------------------------------------

    __slots__ = ["_parameter_core", "_waste_provider", "_warehouse_ms_service", "_brms_service", "_datetime_provider"]

    # !------------------------------------------------------------------------
    # ! info: core atributtes and constructor section start
    # !------------------------------------------------------------------------

    def __init__(self: Self):
        # ** info: cores building
        self._parameter_core: ParameterCore = ParameterCore()
        # ** info: providers building
        self._waste_provider: WasteProvider = WasteProvider()
        # ** info: rest services building
        self._warehouse_ms_service: WarehouseMsService = WarehouseMsService()
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
        warehouse_capacity_and_waste_data = await self._get_warehouse_capacity_and_waste_data(warehouse_id=waste_classify_request.storeId, waste_id=waste_classify_request.wasteId)
        warehouse_current_capacity: float = warehouse_capacity_and_waste_data[0]
        waste_wight_in_kg: float = float(warehouse_capacity_and_waste_data[1].weight_in_kg)
        await self._validate_warehouse_capacity_vs_waste_weight(waste_weight_in_kg=waste_wight_in_kg, warehouse_current_capacity=warehouse_current_capacity)
        new_warehouse_capacity: float = await self._compute_new_warehouse_capacity(warehouse_current_capacity=warehouse_current_capacity, waste_weight_in_kg=waste_wight_in_kg)
        await self._update_warehouse_current_capacity(warehouse_id=waste_classify_request.storeId, new_warehouse_capacity=new_warehouse_capacity)
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
    # ! info: core adapter methods section start
    # ! warning: all the methods in this section are the ones that are going to call methods from another core
    # ! warning: a method only can be declared in this section if it is going to call a port method from another core
    # !------------------------------------------------------------------------

    # ** info: cam pc are initials for core adapter methods parameter core
    async def _cam_pc_get_set_of_parameter_ids_by_domain(self: Self, domain: str) -> Set[int]:
        logging.info("starting _cam_pc_get_set_of_parameter_ids_by_domain")
        ids: Set[int] = await self._parameter_core.cpm_pc_get_set_of_parameter_ids_by_domain(domain=domain)
        logging.info("ending _cam_pc_get_set_of_parameter_ids_by_domain")
        return ids

    # !------------------------------------------------------------------------
    # ! info: core port methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from another core
    # ! warning: a method only can be declared in this section if it is going to be called from another core
    # !------------------------------------------------------------------------

    # ** info: cpm wc are initials for core port methods waste core
    async def cpm_wc_create_waste_with_basic_info(
        self: Self,
        request_uuid: str,
        type: int,
        packaging: int,
        weight_in_kg: float,
        volume_in_l: float,
        description: str,
        note: Union[str, None] = None,
    ) -> Waste:
        logging.info("starting cpm_wc_create_waste_with_basic_info")
        new_waste: Waste = self._waste_provider.create_waste_with_basic_info(
            request_uuid=request_uuid,
            type=type,
            packaging=packaging,
            weight_in_kg=weight_in_kg,
            volume_in_l=volume_in_l,
            description=description,
            note=note,
        )
        logging.info("ending cpm_wc_create_waste_with_basic_info")
        return new_waste

    # ** info: cpm wc are initials for core port methods waste core
    async def cpm_wc_update_waste_status_by_request_id(
        self: Self,
        request_uuid: str,
        process_status: int,
    ) -> list[Waste]:
        logging.info("starting cpm_wc_update_waste_by_requestId")
        updated_wastes: list[Waste] = self._waste_provider.update_waste_status_by_request_id(request_uuid=request_uuid, process_status=process_status)
        logging.info("ending cpm_wc_update_waste_by_requestId")
        return updated_wastes

    # ** info: cpm wc are initials for core port methods waste core
    async def cpm_wc_update_waste_status_and_store_by_request_id(
        self: Self,
        request_uuid: str,
        process_status: int,
        store_id: int,
    ) -> list[Waste]:
        logging.info("starting cpm_wc_update_waste_status_and_store_by_request_id")
        updated_wastes: list[Waste] = self._waste_provider.update_waste_status_and_store_id_by_request_id(
            request_uuid=request_uuid, process_status=process_status, store_id=store_id
        )
        logging.info("ending cpm_wc_update_waste_status_and_store_by_request_id")
        return updated_wastes

    # ** info: cpm wc are initials for core port methods waste core
    async def cpm_wc_check_if_wastes_batch_are_assignable_to_warehouse(
        self: Self,
        warehouse_id: int,
        wastes_ids: list[str],
    ) -> None:
        logging.info("starting cpm_wc_get_warehouse_capacity")
        warehouse_current_capacity, wastes_by_ids = await gather(
            self._get_warehouse_current_capacity(warehouse_id=warehouse_id), self._search_wastes_by_ids(uuids=tuple(wastes_ids))
        )
        wastes_total_weight = await self._compute_wastes_total_weight(wastes=wastes_by_ids)
        if warehouse_current_capacity < wastes_total_weight:
            logging.error(f"warehouse capacity {warehouse_current_capacity} is less than wastes total weight {wastes_total_weight}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"warehouse capacity {warehouse_current_capacity} is less than wastes total weight {wastes_total_weight}"
            )
        logging.info("ending cpm_wc_get_warehouse_capacity")
        return None

    # ** info: cpm wc are initials for core port methods waste core
    async def cpm_get_wastes_by_collect_request_id(self: Self, collect_request_uuid: str) -> list[Waste]:
        logging.info("starting cpm_get_wastes_by_collect_request_id")
        list_wastes_by_collect_request_id: list[Waste] = self._waste_provider.list_wastes_by_collect_request_id(collect_request_uuid=collect_request_uuid)
        logging.info("ending cpm_get_wastes_by_collect_request_id")
        return list_wastes_by_collect_request_id

    async def cpm_wc_copute_new_warehouse_capacity_assigning_new_wastes(self: Self, warehouse_id: int, wastes_ids: list[str]) -> float:
        logging.info("starting cpm_wc_copute_new_warehouse_capacity_assigning_new_wastes")
        warehouse_current_capacity, wastes_by_ids = await gather(
            self._get_warehouse_current_capacity(warehouse_id=warehouse_id), self._search_wastes_by_ids(uuids=tuple(wastes_ids))
        )
        wastes_total_weight = await self._compute_wastes_total_weight(wastes=wastes_by_ids)
        new_warehouse_capacity = await self._compute_new_warehouse_capacity(warehouse_current_capacity=warehouse_current_capacity, waste_weight_in_kg=wastes_total_weight)
        logging.info("ending cpm_wc_copute_new_warehouse_capacity_assigning_new_wastes")
        return new_warehouse_capacity

    async def cpm_wc_update_warehouse_current_capacity(self: Self, warehouse_id: int, new_warehouse_capacity: float) -> float:
        logging.info("starting cpm_wc_update_warehouse_capacity")
        updated_warehouse_capacity = await self._update_warehouse_current_capacity(warehouse_id=warehouse_id, new_warehouse_capacity=new_warehouse_capacity)
        logging.info("ending cpm_wc_update_warehouse_capacity")
        return updated_warehouse_capacity

    # ** info: cpm wc are initials for core port methods waste core
    async def cpm_wc_list_wastes_by_collect_request_id(
        self: Self,
        collect_request_uuid: str,
    ) -> list[Waste]:
        logging.info("starting cpm_wc_list_wastes_by_collect_request_id")
        list_wastes_by_collect_request_id: list[Waste] = self._waste_provider.list_wastes_by_collect_request_id(collect_request_uuid=collect_request_uuid)
        logging.info("ending cpm_wc_list_wastes_by_collect_request_id")
        return list_wastes_by_collect_request_id

    # !------------------------------------------------------------------------
    # ! info: private class methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from inside this core
    # ! warning: a method only can be declared in this section if it is going to be called from inside this core
    # !------------------------------------------------------------------------

    async def _obtain_waste_clasification(self: Self, state_waste: str, weight_in_kg: float, isotopes_number: float) -> int:
        return await self._brms_service.obtain_waste_clasification(state_waste=state_waste, weight_in_kg=weight_in_kg, isotopes_number=isotopes_number)

    async def _map_waste_classify_response(self: Self, clasification: int) -> WasteClasificationResponseDto:
        return WasteClasificationResponseDto(storeType=clasification)

    async def _validate_waste_process_status(self: Self, process_status: int) -> None:
        waste_state_ids: Set[int] = await self._cam_pc_get_set_of_parameter_ids_by_domain(domain=r"wasteProcessStatus")
        if process_status not in waste_state_ids:
            valid_state_waste: str = r",".join(str(s) for s in waste_state_ids)
            logging.error(f"process status {process_status} is not valid valid types are {valid_state_waste}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"process status {process_status} is not valid")

    async def _validate_wastes_state(self: Self, waste_classify_request: WasteClassifyRequestDto) -> None:
        waste_state_ids: Set[int] = await self._cam_pc_get_set_of_parameter_ids_by_domain(domain=r"stateWaste")
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

    async def _get_warehouse_current_capacity(self: Self, warehouse_id: int) -> float:
        return await self._warehouse_ms_service.obtain_warehouse_current_capacity(warehouse_id=warehouse_id)

    async def _get_waste_data_by_id(self: Self, uuid: str) -> Waste:
        waste: Waste = self._waste_provider.search_waste_by_id(uuid=uuid)
        if waste is None:
            logging.error(f"waste with id {uuid} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"waste with id {uuid} not found")
        return waste

    async def _get_warehouse_capacity_and_waste_data(self: Self, warehouse_id: int, waste_id: str) -> tuple[float, Waste]:
        return await gather(self._get_warehouse_current_capacity(warehouse_id=warehouse_id), self._get_waste_data_by_id(uuid=waste_id))

    async def _validate_warehouse_capacity_vs_waste_weight(self: Self, warehouse_current_capacity: float, waste_weight_in_kg: float) -> None:
        if warehouse_current_capacity < waste_weight_in_kg:
            logging.error(f"warehouse capacity {warehouse_current_capacity} is less than waste weight {waste_weight_in_kg}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"warehouse capacity {warehouse_current_capacity} is less than waste weight {waste_weight_in_kg}")

    async def _compute_new_warehouse_capacity(self: Self, warehouse_current_capacity: float, waste_weight_in_kg: float) -> float:
        return warehouse_current_capacity - waste_weight_in_kg

    async def _update_warehouse_current_capacity(self: Self, warehouse_id: int, new_warehouse_capacity: float) -> float:
        return await self._warehouse_ms_service.update_warehouse_current_capacity(warehouse_id=warehouse_id, new_warehouse_capacity=new_warehouse_capacity)

    @async_cached(cache=TTLCache(ttl=240, maxsize=20))
    async def _search_wastes_by_ids(self: Self, uuids: tuple[str, ...]) -> List[Waste]:
        return self._waste_provider.search_wastes_by_ids(uuids=tuple(uuids))

    async def _compute_wastes_total_weight(self: Self, wastes: list[Waste]) -> float:
        return reduce(lambda weight_1, weight_2: weight_1 + weight_2, list(map(lambda waste: float(waste.weight_in_kg), wastes)))
