# !/usr/bin/python3
# type: ignore

# ** info: python imports
from datetime import datetime

# ** info: typing imports
from typing import Self
from typing import List

# ** info: dtos imports
from src.dtos.collect_request_dtos import CollectRequestControllerDtos

CollectRequestCreateResponseDto = CollectRequestControllerDtos.CollectRequestCreateResponseDto
CollectRequestCreateRequestDto = CollectRequestControllerDtos.CollectRequestCreateRequestDto
ResponseRequestDataDto = CollectRequestControllerDtos.ResponseRequestDataDto
ResponseWasteDataDto = CollectRequestControllerDtos.ResponseWasteDataDto

# ** info: providers imports
from src.database.collect_request_provider import CollectRequestProvider
from src.database.waste_provider import WasteProvider

# ** info: users entity
from src.entities.collect_request_entity import CollectRequest
from src.entities.waste_entity import Waste

# ** info: artifacts imports
from src.artifacts.datetime.datetime_provider import datetime_provider

__all__: list[str] = ["CollectRequestController"]


class CollectRequestController:
    def __init__(self: Self):
        # ** info: building controller needed providers
        self.collect_request_provider: CollectRequestProvider = CollectRequestProvider()
        self.waste_provider: WasteProvider = WasteProvider()

    async def driver_request_create(self: Self, request_create_request: CollectRequestCreateRequestDto) -> CollectRequestCreateResponseDto:
        collect_request_id: str = await self._store_collect_request(request_create_request=request_create_request)
        wastes_ids = await self._store_collect_request_wastes(collect_request_id=collect_request_id, request_create_request=request_create_request)
        collect_request_info: CollectRequest = await self._search_collect_request_by_id(collect_request_id=collect_request_id)
        wastes_info: List[Waste] = await self._search_wastes_by_ids(wastes_ids=wastes_ids)
        request_create_response: CollectRequestCreateResponseDto = await self._map_collect_response(
            collect_request_info=collect_request_info, wastes_info=wastes_info
        )
        return request_create_response

    async def _store_collect_request(self: Self, request_create_request: CollectRequestCreateRequestDto) -> str:
        collect_date: datetime = datetime_provider.pretty_date_string_to_date(request_create_request.request.collectDate)
        collect_request_id: str = self.collect_request_provider.store_collect_request(
            collect_date=collect_date, production_center_id=request_create_request.request.productionCenterId
        )
        return collect_request_id

    async def _store_collect_request_wastes(self: Self, collect_request_id: str, request_create_request: CollectRequestCreateRequestDto) -> List[str]:
        wastes_ids: List[str] = list()
        for waste in request_create_request.waste:
            waste_id: Waste = self.waste_provider.store_waste(
                request_uuid=collect_request_id,
                weight_in_kg=waste.weightInKg,
                description=waste.description,
                volume_in_l=waste.volumeInL,
                packaging=waste.packaging,
                type=waste.type,
                note=waste.note,
            )
            wastes_ids.append(waste_id)
        return wastes_ids

    async def _search_collect_request_by_id(self: Self, collect_request_id: str) -> CollectRequest:
        collect_request: CollectRequest = self.collect_request_provider.search_collect_request_by_id(uuid=collect_request_id)
        return collect_request

    async def _search_wastes_by_ids(self: Self, wastes_ids: List[str]) -> List[Waste]:
        wastes: List[Waste] = list()
        for waste_id in wastes_ids:
            waste: Waste = await self._search_waste_by_id(waste_id=waste_id)
            wastes.append(waste)
        return wastes

    async def _search_waste_by_id(self: Self, waste_id: str) -> Waste:
        waste: Waste = self.waste_provider.search_waste_by_id(uuid=waste_id)
        return waste

    async def _map_collect_response(self: Self, collect_request_info: CollectRequest, wastes_info: List[Waste]) -> CollectRequestCreateResponseDto:
        return CollectRequestCreateResponseDto(
            request=await self._map_collect_response_request_info(collect_request_info=collect_request_info),
            waste=await self._map_collect_response_wastes_info(wastes_info=wastes_info),
        )

    async def _map_collect_response_request_info(self: Self, collect_request_info: CollectRequest) -> ResponseRequestDataDto:
        return ResponseRequestDataDto(
            collectDate=datetime_provider.prettify_date_obj(collect_request_info.collect_date),
            productionCenterId=collect_request_info.production_center_id,
            id=collect_request_info.uuid,
        )

    async def _map_collect_response_wastes_info(self: Self, wastes_info: List[Waste]) -> List[ResponseWasteDataDto]:
        collect_response_wastes_info: List[ResponseWasteDataDto] = list()
        for waste_info in wastes_info:
            collect_response_waste_info: ResponseWasteDataDto = await self._map_collect_response_waste_info(waste_info=waste_info)
            collect_response_wastes_info.append(collect_response_waste_info)
        return collect_response_wastes_info

    async def _map_collect_response_waste_info(self: Self, waste_info: Waste) -> ResponseWasteDataDto:
        return ResponseWasteDataDto(
            weightInKg=float(waste_info.weight_in_kg),
            volumeInL=float(waste_info.volume_in_l),
            description=waste_info.description,
            requestId=waste_info.request_uuid,
            packaging=waste_info.packaging,
            note=waste_info.note,
            type=waste_info.type,
            id=waste_info.uuid,
        )
