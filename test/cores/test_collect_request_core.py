# !/usr/bin/python3

# ** info: python imports
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from os.path import join
from pytest import mark
from os import path
import sys

# **info: appending src path to the system paths for absolute imports from src path
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "..", "."))

# ** info: dtos imports
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFullDataResponseDto  # type: ignore
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestFindByStatusResDto  # type: ignore

# ** info: core imports
from src.modules.collect_request.cores.business.collect_request_core import CollectRequestCore  # type: ignore

# ** info: fixtures imports
from test_collect_request_core_fixtures import collect_request_modify_by_id_req_dto_fixture_1  # type: ignore
from test_collect_request_core_fixtures import collect_request_find_by_status_fixture_1  # type: ignore
from test_collect_request_core_fixtures import request_find_request_by_status_fixture_1  # type: ignore
from test_collect_request_core_fixtures import request_full_data_response_fixture_1  # type: ignore
from test_collect_request_core_fixtures import request_create_request_fixture_1  # type: ignore
from test_collect_request_core_fixtures import parameters_ids_fixture_1  # type: ignore
from test_collect_request_core_fixtures import collect_request  # type: ignore
from test_collect_request_core_fixtures import wastes_list  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: building mocks
# ** info: only the methods that interact with external systems are mocked, the rest of the methods are tested
# !! info: this includes only adapters from the same module and cpms (core port methods) from other cores
# ---------------------------------------------------------------------------------------------------------------------

collect_request_core: CollectRequestCore = CollectRequestCore()
type(collect_request_core._parameter_core).cpm_pc_get_set_of_parameter_ids_by_domain = AsyncMock(return_value=parameters_ids_fixture_1)  # type: ignore
collect_request_core._collect_request_provider.find_collects_requests_by_state = MagicMock(return_value=[collect_request])  # type: ignore
collect_request_core._collect_request_provider.modify_collect_request_by_id = MagicMock(return_value=collect_request)
type(collect_request_core._waste_core).cpm_wc_create_waste_with_basic_info = AsyncMock(side_effect=wastes_list)  # type: ignore
type(collect_request_core._waste_core).cpm_wc_update_waste_by_request_id = AsyncMock(return_value=wastes_list)  # type: ignore
collect_request_core._collect_request_provider.store_collect_request = MagicMock(return_value=collect_request)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: executing tests
# ** info: only the drivers are explicitly tested, the rest of the methods are implicitly tested
# ---------------------------------------------------------------------------------------------------------------------


@mark.asyncio
async def test_driver_create_request_hpp1() -> None:
    request_create_response: CollectRequestFullDataResponseDto = await collect_request_core.driver_create_request(request_create_request=request_create_request_fixture_1)
    collect_request_core._collect_request_provider.store_collect_request.assert_called_with(
        collect_date=request_create_request_fixture_1.request.collectDate, production_center_id=request_create_request_fixture_1.request.productionCenterId
    )
    assert request_create_response == request_full_data_response_fixture_1


@mark.asyncio
async def test_driver_find_request_by_status_hpp1() -> None:
    find_request_by_status_response: CollectRequestFindByStatusResDto = await collect_request_core.driver_find_request_by_status(
        request_find_request_by_status=request_find_request_by_status_fixture_1
    )
    collect_request_core._collect_request_provider.find_collects_requests_by_state.assert_called_with(process_status=9)
    assert find_request_by_status_response == collect_request_find_by_status_fixture_1


@mark.asyncio
async def test_driver_modify_request_by_id_hpp1() -> None:
    modify_request_by_id_response: CollectRequestFullDataResponseDto = await collect_request_core.driver_modify_request_by_id(
        request_modify_request_by_id=collect_request_modify_by_id_req_dto_fixture_1
    )
    collect_request_core._collect_request_provider.modify_collect_request_by_id(
        uuid=collect_request_modify_by_id_req_dto_fixture_1.collectReqId,
        process_status=collect_request_modify_by_id_req_dto_fixture_1.processStatus,
        collect_request_note=collect_request_modify_by_id_req_dto_fixture_1.note,
    )
    assert modify_request_by_id_response == request_full_data_response_fixture_1
