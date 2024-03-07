# !/usr/bin/python3

# ** info: python imports
from unittest.mock import MagicMock
from unittest.mock import AsyncMock
from os.path import join
from pytest import mark
from os import path
import sys

# **info: appending src path to the system paths for absolute imports from src path
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "..", "."))

# ** info: dtos imports
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClasificationRequestDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteClassifyRequestDto  # type: ignore

# ** info: core imports
from src.modules.waste.cores.business.waste_core import WasteCore  # type: ignore

# ** info: entities imports
from src.modules.waste.adapters.database_providers_entities.waste_entity import Waste  # type: ignore

# ** info: sidecards.artifacts imports
from src.sidecards.artifacts.datetime_provider import DatetimeProvider  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: create needed artifcts
# ---------------------------------------------------------------------------------------------------------------------

datetime_provider: DatetimeProvider = DatetimeProvider()

# ---------------------------------------------------------------------------------------------------------------------
# ** info: waste fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------------------------------------------
# ** info: building mocks
# ---------------------------------------------------------------------------------------------------------------------

waste_core: WasteCore = WasteCore()
waste_core._brms_service.obtain_waste_clasification = MagicMock(return_value=1)  # type: ignore
waste_core.cam_pc_get_set_of_parameter_ids_by_domain = AsyncMock(return_value=set([1]))  # type: ignore
waste_core._waste_provider.update_waste_internal_classification_info = MagicMock(return_value=waste_1)  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: parameter search request dto fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

parameter_search_request_fixture_1: WasteClasificationRequestDto = WasteClasificationRequestDto(
    stateWaste="liquid",  # type: ignore
    isotopesNumber=1.0,
    weightInKg=1.0,
)

waste_clasification_response_fixture_1: WasteClasificationResponseDto = WasteClasificationResponseDto(
    storeType=1,
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: parameter search request dto fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

update_waste_casification_request_fixture_1: WasteClassifyRequestDto = WasteClassifyRequestDto(
    wasteId="08893dbf-ebd1-4717-988b-fd15ddff12c9",
    isotopesNumber=float(1.0),
    stateWaste=1,
    storeId=1,
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: executing tests
# ---------------------------------------------------------------------------------------------------------------------


@mark.asyncio
async def test_driver_obtain_waste_classify_1() -> None:
    waste_clasification_response: WasteClasificationResponseDto = await waste_core.driver_obtain_waste_classify(parameter_search_request=parameter_search_request_fixture_1)
    waste_core._brms_service.obtain_waste_clasification.assert_called_with(
        state_waste=parameter_search_request_fixture_1.stateWaste,
        isotopes_number=parameter_search_request_fixture_1.isotopesNumber,
        weight_in_kg=parameter_search_request_fixture_1.weightInKg,
    )
    assert waste_clasification_response == waste_clasification_response_fixture_1


@mark.asyncio
async def test_driver_update_waste_classify_classify_1() -> None:
    waste_clasification_response: WasteFullDataResponseDto = await waste_core.driver_update_waste_classify(waste_classify_request=update_waste_casification_request_fixture_1)
    waste_core._brms_service.obtain_waste_clasification.assert_called_with(
        state_waste=parameter_search_request_fixture_1.stateWaste,
        isotopes_number=parameter_search_request_fixture_1.isotopesNumber,
        weight_in_kg=parameter_search_request_fixture_1.weightInKg,
    )
    assert waste_clasification_response == waste_full_data_response_fixture_1
