# !/usr/bin/python3

# ** info: python imports
from os.path import join
from os import path
import sys

# ** info: typing imports
from typing import List

# **info: appending src path to the system paths for absolute imports from src path
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "..", "."))

# ** info: dtos imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFilterByStatusRequestDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationRequestDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseListDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClassifyRequestDto  # type: ignore

# ** info: entities imports
from src.modules.waste.adapters.database_providers_entities.waste_entity import Waste  # type: ignore

# ** info: sidecards.artifacts imports
from src.sidecards.artifacts.datetime_provider import DatetimeProvider  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: create needed artifcts
# ---------------------------------------------------------------------------------------------------------------------

datetime_provider: DatetimeProvider = DatetimeProvider()

# ---------------------------------------------------------------------------------------------------------------------
# ** info: waste entite fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

wastes_list: List[Waste] = list()

waste_1: Waste = Waste(
    uuid="08893dbf-ebd1-4717-988b-fd15ddff12c9",
    request_uuid="9484e5da-0987-45bd-a359-44702769aaad",
    type=1,
    packaging=1,
    weight_in_kg=float(100),  # type: ignore
    volume_in_l=float(100),  # type: ignore
    description="",
    note="",
    process_status=9,
    store=1,
    state_waste=1,
    isotopes_number=float(1.0),  # type: ignore
    create=datetime_provider.get_current_time(),
    update=datetime_provider.get_current_time(),
)

waste_2: Waste = Waste(
    uuid="08893dbf-ebd1-4717-988b-fd15ddff12c9",
    request_uuid="9484e5da-0987-45bd-a359-44702769aaad",
    type=1,
    packaging=1,
    weight_in_kg=float(20),  # type: ignore
    volume_in_l=float(10),  # type: ignore
    description="",
    note="",
    process_status=9,
    store=1,
    state_waste=1,
    isotopes_number=float(4.0),  # type: ignore
    create=datetime_provider.get_current_time(),
    update=datetime_provider.get_current_time(),
)

wastes_list.append(waste_1)
wastes_list.append(waste_2)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: waste full data response dtos declaration
# ---------------------------------------------------------------------------------------------------------------------

waste_full_data_response_fixture_list_1: List[WasteFullDataResponseDto] = list()

waste_full_data_response_fixture_1: WasteFullDataResponseDto = WasteFullDataResponseDto(
    id="08893dbf-ebd1-4717-988b-fd15ddff12c9",
    requestId="9484e5da-0987-45bd-a359-44702769aaad",
    type=1,
    packaging=1,
    processStatus=9,
    weightInKg=100.0,
    volumeInL=100.0,
    isotopesNumber=1.0,
    stateWaste=1,
    storeType=1,
    description="",
    note="",
    create=datetime_provider.prettify_date_time_obj(date_time_obj=waste_1.create),
    update=datetime_provider.prettify_date_time_obj(date_time_obj=waste_1.update),
)

waste_full_data_response_fixture_2: WasteFullDataResponseDto = WasteFullDataResponseDto(
    id="08893dbf-ebd1-4717-988b-fd15ddff12c9",
    requestId="9484e5da-0987-45bd-a359-44702769aaad",
    type=1,
    packaging=1,
    processStatus=9,
    weightInKg=20.0,
    volumeInL=10.0,
    isotopesNumber=4.0,
    stateWaste=1,
    storeType=1,
    description="",
    note="",
    create=datetime_provider.prettify_date_time_obj(date_time_obj=waste_2.create),
    update=datetime_provider.prettify_date_time_obj(date_time_obj=waste_2.update),
)

waste_full_data_response_fixture_list_1.append(waste_full_data_response_fixture_1)
waste_full_data_response_fixture_list_1.append(waste_full_data_response_fixture_2)

waste_full_data_list_response_fixture_1: WasteFullDataResponseListDto = WasteFullDataResponseListDto(values=waste_full_data_response_fixture_list_1)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: parameter search request dtos fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

parameter_search_request_fixture_1: WasteClasificationRequestDto = WasteClasificationRequestDto(
    stateWaste="liquid",  # type: ignore
    isotopesNumber=1.0,
    weightInKg=1.0,
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: waste clasification response dtos fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

waste_clasification_response_fixture_1: WasteClasificationResponseDto = WasteClasificationResponseDto(
    storeType=1,
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: wase classify request dto fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

update_waste_casification_request_fixture_1: WasteClassifyRequestDto = WasteClassifyRequestDto(
    wasteId="08893dbf-ebd1-4717-988b-fd15ddff12c9",
    isotopesNumber=float(1.0),
    stateWaste=1,
    storeId=1,
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: waste filter by status request dto fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

waste_filter_by_status_request_fixture_1: WasteFilterByStatusRequestDto = WasteFilterByStatusRequestDto(
    processStatus=9,
)
