# !/usr/bin/python3

# ** info: python imports
from os.path import join
from os import path
import sys

# ** info: typing imports
from typing import Set

# **info: appending src path to the system paths for absolute imports from src path
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "..", "."))

# ** info: dtos imports
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFindByStatusResDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFindByStatusReqDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestCreateResponseDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestCreateRequestDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import ResponseRequestDataDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import RequestRequestDataDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import ResponseWasteDataDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import RequestWasteDataDto  # type: ignore

# ** info: entities imports
from src.modules.collect_request.adapters.database_providers_entities.collect_request_entity import CollectRequest  # type: ignore
from src.modules.waste.adapters.database_providers_entities.waste_entity import Waste  # type: ignore

# ** info: sidecards.artifacts imports
from src.sidecards.artifacts.datetime_provider import DatetimeProvider  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: create needed artifcts
# ---------------------------------------------------------------------------------------------------------------------

datetime_provider: DatetimeProvider = DatetimeProvider()

# ---------------------------------------------------------------------------------------------------------------------
# ** info: create request fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

request_waste_data_dto_list_fixture_1: list[RequestWasteDataDto] = list()

request_waste_data_dto_fixture_1: RequestWasteDataDto = RequestWasteDataDto(
    weightInKg=100.00,
    volumeInL=100.00,
    description="",
    packaging=1,
    type=1,
)

request_waste_data_dto_fixture_2: RequestWasteDataDto = RequestWasteDataDto(
    weightInKg=40.00,
    volumeInL=60.00,
    description="",
    packaging=1,
    type=1,
)

request_waste_data_dto_list_fixture_1.append(request_waste_data_dto_fixture_1)
request_waste_data_dto_list_fixture_1.append(request_waste_data_dto_fixture_2)

request_request_data_dto_fixture_1: RequestRequestDataDto = RequestRequestDataDto(productionCenterId=10122012334, collectDate=r"01/01/2021")

request_create_request_fixture_1: CollectRequestCreateRequestDto = CollectRequestCreateRequestDto(
    waste=request_waste_data_dto_list_fixture_1,
    request=request_request_data_dto_fixture_1,
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: parameters fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

parameters_ids_fixture_1: Set[int] = set([1, 2])

# ---------------------------------------------------------------------------------------------------------------------
# ** info: more needed fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

wastes_ids_fixture_1: list[str] = ["9484e5da-0987-45bd-a359-44702769aaad", "a129fddc-0caf-43c8-9028-e67e5572bf84"]
collect_request_uuid_fixture_1: str = "b033df08-3846-40d3-a82c-0af148b7027a"

# ---------------------------------------------------------------------------------------------------------------------
# ** info: building entities fixtures
# ---------------------------------------------------------------------------------------------------------------------

wastes_list: list[Waste] = list()

waste_1: Waste = Waste(
    uuid=wastes_ids_fixture_1[0],
    request_uuid=collect_request_uuid_fixture_1,
    type=request_waste_data_dto_list_fixture_1[0].type,
    packaging=request_waste_data_dto_list_fixture_1[0].packaging,
    weight_in_kg=float(request_waste_data_dto_list_fixture_1[0].weightInKg),  # type: ignore
    volume_in_l=float(request_waste_data_dto_list_fixture_1[0].volumeInL),  # type: ignore
    description=request_waste_data_dto_list_fixture_1[0].description,
    note=request_waste_data_dto_list_fixture_1[0].note,
    process_status=9,
    store=9,
    state_waste=9,
    isotopes_number=float(9),  # type: ignore
    create=datetime_provider.get_current_time(),
    update=datetime_provider.get_current_time(),
)

waste_2: Waste = Waste(
    uuid=wastes_ids_fixture_1[1],
    request_uuid=collect_request_uuid_fixture_1,
    type=request_waste_data_dto_list_fixture_1[1].type,
    packaging=request_waste_data_dto_list_fixture_1[1].packaging,
    weight_in_kg=float(request_waste_data_dto_list_fixture_1[1].weightInKg),  # type: ignore
    volume_in_l=float(request_waste_data_dto_list_fixture_1[1].volumeInL),  # type: ignore
    description=request_waste_data_dto_list_fixture_1[1].description,
    note=request_waste_data_dto_list_fixture_1[1].note,
    process_status=9,
    store=9,
    state_waste=9,
    isotopes_number=float(9),  # type: ignore
    create=datetime_provider.get_current_time(),
    update=datetime_provider.get_current_time(),
)

wastes_list.append(waste_1)
wastes_list.append(waste_2)

collect_request: CollectRequest = CollectRequest(
    collect_date=datetime_provider.pretty_date_string_to_date(iso_string=r"01/01/2021"),
    production_center_id=request_request_data_dto_fixture_1.productionCenterId,
    uuid=collect_request_uuid_fixture_1,
    process_status=9,
    create=datetime_provider.get_current_time(),
    update=datetime_provider.get_current_time(),
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: create response fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

response_waste_data_dto_list_fixture_1: list[ResponseWasteDataDto] = list()

response_waste_data_dto_fixture_1: ResponseWasteDataDto = ResponseWasteDataDto(
    weightInKg=waste_1.weight_in_kg,  # type: ignore
    volumeInL=waste_1.volume_in_l,  # type: ignore
    description=waste_1.description,
    packaging=waste_1.packaging,
    requestId=waste_1.request_uuid,
    type=waste_1.type,
    note=waste_1.note,
    id=waste_1.uuid,
    processStatus=9,
    create=datetime_provider.prettify_date_time_obj(date_time_obj=waste_1.create),
    update=datetime_provider.prettify_date_time_obj(date_time_obj=waste_1.update),
)

response_waste_data_dto_fixture_2: ResponseWasteDataDto = ResponseWasteDataDto(
    weightInKg=waste_2.weight_in_kg,  # type: ignore
    volumeInL=waste_2.volume_in_l,  # type: ignore
    description=waste_2.description,
    packaging=waste_2.packaging,
    requestId=waste_2.request_uuid,
    type=waste_2.type,
    note=waste_2.note,
    id=waste_2.uuid,
    processStatus=9,
    create=datetime_provider.prettify_date_time_obj(date_time_obj=waste_2.create),
    update=datetime_provider.prettify_date_time_obj(date_time_obj=waste_2.update),
)

response_waste_data_dto_list_fixture_1.append(response_waste_data_dto_fixture_1)
response_waste_data_dto_list_fixture_1.append(response_waste_data_dto_fixture_2)

response_request_data_dto_fixture_1: ResponseRequestDataDto = ResponseRequestDataDto(
    productionCenterId=collect_request.production_center_id,
    collectDate=r"01/01/2021",
    id=collect_request.uuid,
    processStatus=9,
    create=datetime_provider.prettify_date_time_obj(date_time_obj=collect_request.create),
    update=datetime_provider.prettify_date_time_obj(date_time_obj=collect_request.update),
)

request_create_response_fixture_1: CollectRequestCreateResponseDto = CollectRequestCreateResponseDto(
    waste=response_waste_data_dto_list_fixture_1,
    request=response_request_data_dto_fixture_1,
)

request_find_request_by_status_fixture_1: CollectRequestFindByStatusReqDto = CollectRequestFindByStatusReqDto(processStatus=9)

collect_request_find_by_status_fixture_1: CollectRequestFindByStatusResDto = CollectRequestFindByStatusResDto(values=[response_request_data_dto_fixture_1])
