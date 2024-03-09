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
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseListDto  # type: ignore
from src.modules.waste.ports.rest_routers_dtos.waste_dtos import WasteFullDataResponseDto  # type: ignore

# ** info: core imports
from src.modules.waste.cores.business.waste_core import WasteCore  # type: ignore

# ** info: fixtures imports
from test_waste_core_fixtures import update_waste_casification_request_fixture_1  # type: ignore
from test_waste_core_fixtures import waste_filter_by_status_request_fixture_1  # type: ignore
from test_waste_core_fixtures import waste_full_data_list_response_fixture_1  # type: ignore
from test_waste_core_fixtures import waste_clasification_response_fixture_1  # type: ignore
from test_waste_core_fixtures import waste_update_status_request_fixture_1  # type: ignore
from test_waste_core_fixtures import parameter_search_request_fixture_1  # type: ignore
from test_waste_core_fixtures import waste_full_data_response_fixture_1  # type: ignore
from test_waste_core_fixtures import waste_full_data_response_fixture_2  # type: ignore
from test_waste_core_fixtures import wastes_list  # type: ignore
from test_waste_core_fixtures import waste_1  # type: ignore
from test_waste_core_fixtures import waste_2  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: building mocks
# ** info: only the methods that interact with external systems are mocked, the rest of the methods are tested
# !! info: this includes only adapters from the same module and cpms (core port methods) from other cores
# ---------------------------------------------------------------------------------------------------------------------

waste_core: WasteCore = WasteCore()
waste_core._parameter_core.cpm_pc_get_set_of_parameter_ids_by_domain = AsyncMock(return_value=set([1, 9]))  # type: ignore
waste_core._waste_provider.update_waste_internal_classification_info = MagicMock(return_value=waste_1)  # type: ignore
waste_core._waste_provider.list_wastes_by_process_status = MagicMock(return_value=wastes_list)  # type: ignore
waste_core._waste_provider.update_waste_status = MagicMock(return_value=waste_2)  # type: ignore
waste_core._brms_service.obtain_waste_clasification = AsyncMock(return_value=1)  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: executing tests
# ** info: only the drivers are explicitly tested, the rest of the methods are implicitly tested
# ---------------------------------------------------------------------------------------------------------------------


@mark.asyncio
async def test_driver_obtain_waste_classify_hpp1() -> None:
    obtain_waste_classify_response: WasteClasificationResponseDto = await waste_core.driver_obtain_waste_classify(parameter_search_request=parameter_search_request_fixture_1)
    waste_core._brms_service.obtain_waste_clasification.assert_called_with(
        state_waste=parameter_search_request_fixture_1.stateWaste,
        isotopes_number=parameter_search_request_fixture_1.isotopesNumber,
        weight_in_kg=parameter_search_request_fixture_1.weightInKg,
    )
    assert obtain_waste_classify_response == waste_clasification_response_fixture_1


@mark.asyncio
async def test_driver_update_waste_classify_classify_hpp1() -> None:
    update_waste_classify_response: WasteFullDataResponseDto = await waste_core.driver_update_waste_classify(waste_classify_request=update_waste_casification_request_fixture_1)
    waste_core._brms_service.obtain_waste_clasification.assert_called_with(
        state_waste=parameter_search_request_fixture_1.stateWaste,
        isotopes_number=parameter_search_request_fixture_1.isotopesNumber,
        weight_in_kg=parameter_search_request_fixture_1.weightInKg,
    )
    assert update_waste_classify_response == waste_full_data_response_fixture_1


@mark.asyncio
async def test_driver_search_waste_by_status_hpp1() -> None:
    filtered_wastes_response: WasteFullDataResponseListDto = await waste_core.driver_search_waste_by_status(filter_waste_by_status_request=waste_filter_by_status_request_fixture_1)
    waste_core._waste_provider.list_wastes_by_process_status.assert_called_with(process_status=9)
    assert filtered_wastes_response == waste_full_data_list_response_fixture_1


@mark.asyncio
async def test_driver_update_waste_status_hpp1() -> None:
    waste_update_status_response: WasteFullDataResponseDto = await waste_core.driver_update_waste_status(waste_update_status_request=waste_update_status_request_fixture_1)
    waste_core._waste_provider.list_wastes_by_process_status.assert_called_with(process_status=9)
    assert waste_update_status_response == waste_full_data_response_fixture_2
