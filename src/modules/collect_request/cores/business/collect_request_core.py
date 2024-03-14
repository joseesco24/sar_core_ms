# !/usr/bin/python3

# ** info: python imports
import logging

# ** info: asyncio imports
from asyncio import gather

# ** info: typing imports
from typing import Self
from typing import List
from typing import Set

# ** info: fastapi imports
from fastapi import HTTPException
from fastapi import status

# ** info: cores imports
from src.modules.parameter.cores.business.parameter_core import ParameterCore  # type: ignore
from src.modules.waste.cores.business.waste_core import WasteCore  # type: ignore

# ** info: dtos imports
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFindByStatusReqDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFindByStatusResDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFullDataResponseDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestCreateRequestDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestModifyByIdReqDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import ResponseRequestDataDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import ResponseWasteDataDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestIdDto  # type: ignore

# ** info: entities imports
from src.modules.collect_request.adapters.database_providers_entities.collect_request_entity import CollectRequest  # type: ignore
from src.modules.waste.adapters.database_providers_entities.waste_entity import Waste  # type: ignore

# ** info: providers imports
from src.modules.collect_request.adapters.database_providers.collect_request_provider import CollectRequestProvider  # type: ignore

# ** info: sidecards.artifacts imports
from src.business_sidecards.artifacts.business_glossary_translate_provider import BusinessGlossaryTranslateProvider  # type: ignore
from src.business_sidecards.constants.collect_request_states_constants import CollectRequestStates  # type: ignore
from src.general_sidecards.artifacts.datetime_provider import DatetimeProvider  # type: ignore

__all__: list[str] = ["CollectRequestCore"]


class CollectRequestCore:

    # !------------------------------------------------------------------------
    # ! info: core slots section start
    # !------------------------------------------------------------------------

    __slots__ = ["_parameter_core", "_waste_core", "_collect_request_provider", "_business_glossary_translate_provider", "_datetime_provider"]

    # !------------------------------------------------------------------------
    # ! info: core atributtes and constructor section start
    # !------------------------------------------------------------------------

    def __init__(self: Self):
        # ** info: cores building
        self._parameter_core: ParameterCore = ParameterCore()
        self._waste_core: WasteCore = WasteCore()
        # ** info: providers building
        self._collect_request_provider: CollectRequestProvider = CollectRequestProvider()
        # ** info: sidecards building
        self._business_glossary_translate_provider: BusinessGlossaryTranslateProvider = BusinessGlossaryTranslateProvider()
        self._datetime_provider: DatetimeProvider = DatetimeProvider()

    # !------------------------------------------------------------------------
    # ! info: driver methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from the routers layer
    # ! warning: a method only can be declared in this section if it is going to be called from the routers layer
    # !------------------------------------------------------------------------

    async def driver_create_request(self: Self, request_create_request: CollectRequestCreateRequestDto) -> CollectRequestFullDataResponseDto:
        logging.info("starting driver_create_request")
        await self._validate_wastes_domains(request_create_request=request_create_request)
        collect_request_info: CollectRequest = await self._store_collect_request(request_create_request=request_create_request)
        wastes_info: List[Waste] = await self._cam_wc_create_waste_with_basic_info(collect_request_id=collect_request_info.uuid, request_create_request=request_create_request)
        request_create_response: CollectRequestFullDataResponseDto = await self._map_collect_response(collect_request_info=collect_request_info, wastes_info=wastes_info)
        logging.info("starting driver_create_request")
        return request_create_response

    async def driver_find_request_by_status(self: Self, request_find_request_by_status: CollectRequestFindByStatusReqDto) -> CollectRequestFindByStatusResDto:
        logging.info("starting driver_find_request_by_status")
        await self._validate_collect_request_process_status(process_status=request_find_request_by_status.processStatus)
        collect_request_info: List[CollectRequest] = self._collect_request_provider.find_collects_requests_by_state(process_status=request_find_request_by_status.processStatus)
        find_request_by_status_response: CollectRequestFindByStatusResDto = await self._map_full_collect_response_list(collect_request_info=collect_request_info)
        logging.info("driver_find_request_by_status ended")
        return find_request_by_status_response

    async def driver_modify_request_by_id(self: Self, request_modify_request_by_id: CollectRequestModifyByIdReqDto) -> CollectRequestFullDataResponseDto:
        logging.info("starting driver_modify_request_by_id")
        await self._validate_collect_request_process_status(process_status=request_modify_request_by_id.processStatus)
        collect_request_info, wastes_info = await self._update_collect_request_and_child_wastes_at_once(
            collect_request_new_status=request_modify_request_by_id.processStatus,
            collect_request_id=request_modify_request_by_id.collectReqId,
        )
        request_create_response: CollectRequestFullDataResponseDto = await self._map_collect_response(collect_request_info=collect_request_info, wastes_info=wastes_info)
        logging.info("driver_modify_request_by_id ended")
        return request_create_response

    async def driver_set_collect_request_to_finished(self: Self, collect_request_just_id_req: CollectRequestIdDto) -> CollectRequestFullDataResponseDto:
        logging.info("starting driver_set_collect_request_to_finished")
        collect_request_info, wastes_info = await self._update_collect_request_and_child_wastes_at_once(
            collect_request_id=collect_request_just_id_req.collectReqId,
            collect_request_new_status=CollectRequestStates.finished,
        )
        request_create_response: CollectRequestFullDataResponseDto = await self._map_collect_response(collect_request_info=collect_request_info, wastes_info=wastes_info)
        logging.info("driver_set_collect_request_to_finished ended")
        return request_create_response

    async def driver_set_collect_request_to_approved(self: Self, collect_request_just_id_req: CollectRequestIdDto) -> CollectRequestFullDataResponseDto:
        logging.info("starting driver_set_collect_request_to_approved")
        collect_request_info, wastes_info = await self._update_collect_request_and_child_wastes_at_once(
            collect_request_id=collect_request_just_id_req.collectReqId,
            collect_request_new_status=CollectRequestStates.approved,
        )
        request_create_response: CollectRequestFullDataResponseDto = await self._map_collect_response(collect_request_info=collect_request_info, wastes_info=wastes_info)
        logging.info("driver_set_collect_request_to_approved ended")
        return request_create_response

    async def driver_set_collect_request_to_rejected(self: Self, collect_request_just_id_req: CollectRequestIdDto) -> CollectRequestFullDataResponseDto:
        logging.info("starting api_set_collect_request_to_rejected")
        collect_request_info, wastes_info = await self._update_collect_request_and_child_wastes_at_once(
            collect_request_id=collect_request_just_id_req.collectReqId,
            collect_request_new_status=CollectRequestStates.rejected,
        )
        request_create_response: CollectRequestFullDataResponseDto = await self._map_collect_response(collect_request_info=collect_request_info, wastes_info=wastes_info)
        logging.info("api_set_collect_request_to_rejected ended")
        return request_create_response

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

    # ** info: cam wc are initials for core adapter methods waste core
    async def _cam_wc_create_waste_with_basic_info(self: Self, collect_request_id: str, request_create_request: CollectRequestCreateRequestDto) -> List[Waste]:
        logging.info("starting cpm_wc_create_waste_with_basic_info")
        wastes: List[Waste] = []
        for waste in request_create_request.waste:
            waste_info: Waste = await self._waste_core.cpm_wc_create_waste_with_basic_info(
                request_uuid=collect_request_id,
                weight_in_kg=waste.weightInKg,
                description=waste.description,
                volume_in_l=waste.volumeInL,
                packaging=waste.packaging,
                type=waste.type,
                note=waste.note,
            )
            wastes.append(waste_info)
        logging.info("ending cpm_wc_create_waste_with_basic_info")
        return wastes

    # ** info: cam wc are initials for core adapter methods waste core
    async def _cam_wc_update_waste_by_request_id(self: Self, collect_request_id: str, process_status_waste: int) -> list[Waste]:
        logging.info("starting _cam_wc_update_waste_by_request_id")
        updated_wastes: list[Waste] = await self._waste_core.cpm_wc_update_waste_by_request_id(request_uuid=collect_request_id, process_status=process_status_waste)
        logging.info("ending _cam_wc_update_waste_by_request_id")
        return updated_wastes

    # ** info: cam wc are initials for core adapter methods waste core
    async def _cam_wc_list_wastes_by_collect_request_id(self: Self, collect_request_uuid: str) -> list[Waste]:
        logging.info("starting _cam_wc_list_wastes_by_collect_request_id")
        list_wastes_by_collect_request_id: list[Waste] = await self._waste_core.cpm_wc_list_wastes_by_collect_request_id(collect_request_uuid=collect_request_uuid)
        logging.info("ending _cam_wc_list_wastes_by_collect_request_id")
        return list_wastes_by_collect_request_id

    # !------------------------------------------------------------------------
    # ! info: core port methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from another core
    # ! warning: a method only can be declared in this section if it is going to be called from another core
    # !------------------------------------------------------------------------

    # !------------------------------------------------------------------------
    # ! info: private class methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from inside this core
    # ! warning: a method only can be declared in this section if it is going to be called from inside this core
    # !------------------------------------------------------------------------

    async def _validate_wastes_domains(self: Self, request_create_request: CollectRequestCreateRequestDto) -> None:
        waste_packaging_types_ids: Set[int] = await self._cam_pc_get_set_of_parameter_ids_by_domain(domain=r"wastePackagingType")
        waste_types_ids: Set[int] = await self._cam_pc_get_set_of_parameter_ids_by_domain(domain=r"wasteType")
        for waste in request_create_request.waste:
            if waste.packaging not in waste_packaging_types_ids:
                valid_waste_types: str = r",".join(str(s) for s in waste_packaging_types_ids)
                logging.error(f"packaging type {waste.packaging} is not valid valid types are {valid_waste_types}")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"packaging type {waste.packaging} is not valid")
            if waste.type not in waste_types_ids:
                valid_packaging_types: str = r",".join(str(s) for s in waste_types_ids)
                logging.error(f"waste type {waste.packaging} is not valid valid types are {valid_packaging_types}")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"waste type {waste.type} is not valid")

    async def _store_collect_request(self: Self, request_create_request: CollectRequestCreateRequestDto) -> CollectRequest:
        collect_request_info: CollectRequest = self._collect_request_provider.store_collect_request(
            collect_date=request_create_request.request.collectDate, production_center_id=request_create_request.request.productionCenterId
        )
        return collect_request_info

    async def _modify_collect_request(self: Self, collect_request_id: str, process_status: int) -> CollectRequest:
        collect_request_info: CollectRequest = self._collect_request_provider.modify_collect_request_by_id(uuid=collect_request_id, process_status=process_status)
        return collect_request_info

    async def _validate_collect_request_process_status(self: Self, process_status: int) -> None:
        collect_state_ids: Set[int] = await self._cam_pc_get_set_of_parameter_ids_by_domain(domain=r"collectRequestProcessStatus")
        if process_status not in collect_state_ids:
            valid_state_collect: str = r",".join(str(s) for s in collect_state_ids)
            logging.error(f"process status {process_status} is not valid valid types are {valid_state_collect}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"process status {process_status} is not valid")

    async def _map_collect_response(self: Self, collect_request_info: CollectRequest, wastes_info: List[Waste]) -> CollectRequestFullDataResponseDto:
        return CollectRequestFullDataResponseDto(
            request=await self._map_collect_response_request_info(collect_request_info=collect_request_info),
            waste=await self._map_collect_response_wastes_info(wastes_info=wastes_info),
        )

    async def _map_full_collect_response_list(self: Self, collect_request_info: List[CollectRequest]) -> CollectRequestFindByStatusResDto:
        return CollectRequestFindByStatusResDto(values=await self._map_full_collect_responses(collect_request_info=collect_request_info))

    async def _map_full_collect_responses(self: Self, collect_request_info: List[CollectRequest]) -> List[ResponseRequestDataDto]:
        return [await self._map_full_collect_response(collect_request_info=collect_request_info) for collect_request_info in collect_request_info]

    async def _map_full_collect_response(self: Self, collect_request_info: CollectRequest) -> ResponseRequestDataDto:
        created: str = self._datetime_provider.prettify_date_time_obj(date_time_obj=collect_request_info.create)
        updated: str = self._datetime_provider.prettify_date_time_obj(date_time_obj=collect_request_info.update)
        CollectRequest_full_data_response: ResponseRequestDataDto = ResponseRequestDataDto(
            id=collect_request_info.uuid,
            collectDate=self._datetime_provider.prettify_date_obj(collect_request_info.collect_date),
            processStatus=collect_request_info.process_status,
            productionCenterId=collect_request_info.production_center_id,
            update=updated,
            create=created,
        )
        return CollectRequest_full_data_response

    async def _map_collect_response_request_info(self: Self, collect_request_info: CollectRequest) -> ResponseRequestDataDto:
        create: str = self._datetime_provider.prettify_date_time_obj(date_time_obj=collect_request_info.create)
        update: str = self._datetime_provider.prettify_date_time_obj(date_time_obj=collect_request_info.update)
        return ResponseRequestDataDto(
            id=collect_request_info.uuid,
            collectDate=self._datetime_provider.prettify_date_obj(collect_request_info.collect_date),
            processStatus=collect_request_info.process_status,
            productionCenterId=collect_request_info.production_center_id,
            update=update,
            create=create,
        )

    async def _map_collect_response_wastes_info(self: Self, wastes_info: List[Waste]) -> List[ResponseWasteDataDto]:
        collect_response_wastes_info: List[ResponseWasteDataDto] = list()
        for waste_info in wastes_info:
            collect_response_waste_info: ResponseWasteDataDto = await self._map_collect_response_waste_info(waste_info=waste_info)
            collect_response_wastes_info.append(collect_response_waste_info)
        return collect_response_wastes_info

    async def _map_collect_response_waste_info(self: Self, waste_info: Waste) -> ResponseWasteDataDto:
        created: str = self._datetime_provider.prettify_date_time_obj(date_time_obj=waste_info.create)
        updated: str = self._datetime_provider.prettify_date_time_obj(date_time_obj=waste_info.update)
        return ResponseWasteDataDto(
            id=waste_info.uuid,
            requestId=waste_info.request_uuid,
            type=waste_info.type,
            packaging=waste_info.packaging,
            processStatus=waste_info.process_status,
            weightInKg=float(waste_info.weight_in_kg),
            volumeInL=float(waste_info.volume_in_l),
            isotopesNumber=None,
            stateWaste=None,
            storeType=None,
            description=waste_info.description,
            note=waste_info.note,
            create=created,
            update=updated,
        )

    async def _select_waste_status_by_collect_request_status(self: Self, process_status: int) -> int:
        return await self._business_glossary_translate_provider.select_waste_status_by_collect_request_status(collect_request_status=process_status)

    async def _update_collect_request_and_child_wastes_at_once(self: Self, collect_request_id: str, collect_request_new_status: int) -> tuple[CollectRequest, list[Waste]]:
        updated_waste_status: int = await self._select_waste_status_by_collect_request_status(process_status=collect_request_new_status)
        return await gather(
            self._modify_collect_request(collect_request_id=collect_request_id, process_status=collect_request_new_status),
            self._cam_wc_update_waste_by_request_id(collect_request_id=collect_request_id, process_status_waste=updated_waste_status),
        )
