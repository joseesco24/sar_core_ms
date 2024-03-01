# !/usr/bin/python3
# type: ignore

# ** info: python imports
from unittest.mock import MagicMock
from unittest.mock import call
from os.path import join
from pytest import mark
from os import path
import sys

# ** info: fastapi imports
from fastapi import HTTPException

# **info: appending src path to the system paths for absolute imports from src path
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "..", "."))

# ** info: dtos imports
from src.modules.collect_request.ports.rest_routers_dtos.collect_request_dtos import CollectRequestControllerDtos

CollectRequestCreateResponseDto = CollectRequestControllerDtos.CollectRequestCreateResponseDto
CollectRequestCreateRequestDto = CollectRequestControllerDtos.CollectRequestCreateRequestDto
ResponseRequestDataDto = CollectRequestControllerDtos.ResponseRequestDataDto
RequestRequestDataDto = CollectRequestControllerDtos.RequestRequestDataDto
ResponseWasteDataDto = CollectRequestControllerDtos.ResponseWasteDataDto
RequestWasteDataDto = CollectRequestControllerDtos.RequestWasteDataDto

# ** info: core imports
from src.modules.collect_request.cores.business.collect_request_core import CollectRequestCore

# ** info: entities imports
from src.modules.collect_request.adapters.database_providers_entities.collect_request_entity import CollectRequest
from src.modules.parameter.adapters.database_providers_entities.parameter_entity import Parameter
from src.modules.waste.adapters.database_providers_entities.waste_entity import Waste

# ** info: artifacts imports
from src.sidecards.artifacts.datetime_provider import DatetimeProvider

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
    packaging=2,
    type=2,
)

request_waste_data_dto_list_fixture_1.append(request_waste_data_dto_fixture_1)
request_waste_data_dto_list_fixture_1.append(request_waste_data_dto_fixture_2)

request_request_data_dto_fixture_1: RequestRequestDataDto = RequestRequestDataDto(productionCenterId=10122012334, collectDate=r"01/01/2021")

request_create_request_fixture_1: CollectRequestCreateRequestDto = CollectRequestCreateRequestDto(
    waste=request_waste_data_dto_list_fixture_1,
    request=request_request_data_dto_fixture_1,
)


# ---------------------------------------------------------------------------------------------------------------------
# ** info: parameter fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

parameter_list_fixture_1: list[Parameter] = list()

parameter_fixture_1: Parameter = Parameter(
    id=1,
    domain=r"wasteType",
    value=r"Radioterapia",
    description=r"Residuos provenientes del equipo empleado en el tratamiento de diversos tipos de cáncer, como el de mama, próstata y pulmón",
    active=True,
)

parameter_fixture_2: Parameter = Parameter(
    id=2,
    domain=r"wasteType",
    value=r"Combustible Nuclear",
    description=r"Residuos provenientes de reactores nucleares en los que se usa material nuclear para generar energía eléctrica",
    active=True,
)

parameter_list_fixture_1.append(parameter_fixture_1)
parameter_list_fixture_1.append(parameter_fixture_2)

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
    weight_in_kg=request_waste_data_dto_list_fixture_1[0].weightInKg,
    volume_in_l=request_waste_data_dto_list_fixture_1[0].volumeInL,
    description=request_waste_data_dto_list_fixture_1[0].description,
    note=request_waste_data_dto_list_fixture_1[0].note,
)

waste_2: Waste = Waste(
    uuid=wastes_ids_fixture_1[1],
    request_uuid=collect_request_uuid_fixture_1,
    type=request_waste_data_dto_list_fixture_1[1].type,
    packaging=request_waste_data_dto_list_fixture_1[1].packaging,
    weight_in_kg=request_waste_data_dto_list_fixture_1[1].weightInKg,
    volume_in_l=request_waste_data_dto_list_fixture_1[1].volumeInL,
    description=request_waste_data_dto_list_fixture_1[1].description,
    note=request_waste_data_dto_list_fixture_1[1].note,
)

wastes_list.append(waste_1)
wastes_list.append(waste_2)

collect_request: CollectRequest = CollectRequest(
    collect_date=datetime_provider.pretty_date_string_to_date(iso_string=r"01/01/2021"),
    production_center_id=request_request_data_dto_fixture_1.productionCenterId,
    uuid=collect_request_uuid_fixture_1,
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: create response fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

response_waste_data_dto_list_fixture_1: list[ResponseWasteDataDto] = list()

response_waste_data_dto_fixture_1: ResponseWasteDataDto = ResponseWasteDataDto(
    weightInKg=waste_1.weight_in_kg,
    volumeInL=waste_1.volume_in_l,
    description=waste_1.description,
    packaging=waste_1.packaging,
    requestId=waste_1.request_uuid,
    type=waste_1.type,
    note=waste_1.note,
    id=waste_1.uuid,
)

response_waste_data_dto_fixture_2: ResponseWasteDataDto = ResponseWasteDataDto(
    weightInKg=waste_2.weight_in_kg,
    volumeInL=waste_2.volume_in_l,
    description=waste_2.description,
    packaging=waste_2.packaging,
    requestId=waste_2.request_uuid,
    type=waste_2.type,
    note=waste_2.note,
    id=waste_2.uuid,
)

response_waste_data_dto_list_fixture_1.append(response_waste_data_dto_fixture_1)
response_waste_data_dto_list_fixture_1.append(response_waste_data_dto_fixture_2)

response_request_data_dto_fixture_1: ResponseRequestDataDto = ResponseRequestDataDto(
    productionCenterId=collect_request.production_center_id,
    collectDate=r"01/01/2021",
    id=collect_request.uuid,
)

request_create_response_fixture_1: CollectRequestCreateResponseDto = CollectRequestCreateResponseDto(
    waste=response_waste_data_dto_list_fixture_1,
    request=response_request_data_dto_fixture_1,
)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: building mocks
# ---------------------------------------------------------------------------------------------------------------------

collect_request_core: CollectRequestCore = CollectRequestCore()
collect_request_core.collect_request_provider.store_collect_request = MagicMock(return_value=collect_request_uuid_fixture_1)
collect_request_core.parameter_provider.search_parameters_by_domain = MagicMock(return_value=parameter_list_fixture_1)
collect_request_core.waste_provider.store_waste = MagicMock(side_effect=wastes_ids_fixture_1)
collect_request_core.collect_request_provider.search_collect_request_by_id = MagicMock(return_value=collect_request)
collect_request_core.waste_provider.search_waste_by_id = MagicMock(side_effect=wastes_list)

# ---------------------------------------------------------------------------------------------------------------------
# ** info: executing tests
# ---------------------------------------------------------------------------------------------------------------------


@mark.asyncio
async def test_validate_wastes_domains_1() -> None:
    try:
        await collect_request_core._validate_wastes_domains(request_create_request=request_create_request_fixture_1)
    except HTTPException:
        assert False


@mark.asyncio
async def test_validate_wastes_domains_2() -> None:
    request_waste_data_dto_fixture_1.packaging = 3
    try:
        await collect_request_core._validate_wastes_domains(request_create_request=request_create_request_fixture_1)
    except HTTPException:
        assert True
    request_waste_data_dto_fixture_1.packaging = 1


@mark.asyncio
async def test_store_collect_request_1() -> None:
    collect_request_id: str = await collect_request_core._store_collect_request(request_create_request=request_create_request_fixture_1)
    assert collect_request_id == collect_request_uuid_fixture_1
    collect_request_core.collect_request_provider.store_collect_request.assert_called_with(
        collect_date=request_create_request_fixture_1.request.collectDate, production_center_id=request_create_request_fixture_1.request.productionCenterId
    )


@mark.asyncio
async def test_store_collect_request_wastes_1() -> None:
    wastes_ids: list[str] = await collect_request_core._store_collect_request_wastes(
        collect_request_id=collect_request_uuid_fixture_1, request_create_request=request_create_request_fixture_1
    )
    assert wastes_ids == wastes_ids_fixture_1
    calls = [
        call(
            request_uuid=collect_request_uuid_fixture_1,
            weight_in_kg=request_create_request_fixture_1.waste[0].weightInKg,
            description=request_create_request_fixture_1.waste[0].description,
            volume_in_l=request_create_request_fixture_1.waste[0].volumeInL,
            packaging=request_create_request_fixture_1.waste[0].packaging,
            type=request_create_request_fixture_1.waste[0].type,
            note=request_create_request_fixture_1.waste[0].note,
        ),
        call(
            request_uuid=collect_request_uuid_fixture_1,
            weight_in_kg=request_create_request_fixture_1.waste[1].weightInKg,
            description=request_create_request_fixture_1.waste[1].description,
            volume_in_l=request_create_request_fixture_1.waste[1].volumeInL,
            packaging=request_create_request_fixture_1.waste[1].packaging,
            type=request_create_request_fixture_1.waste[1].type,
            note=request_create_request_fixture_1.waste[1].note,
        ),
    ]
    collect_request_core.waste_provider.store_waste.assert_has_calls(calls)


@mark.asyncio
async def test_search_collect_request_by_id_1() -> None:
    await collect_request_core._search_collect_request_by_id(collect_request_id=collect_request_uuid_fixture_1)
    collect_request_core.collect_request_provider.search_collect_request_by_id.assert_called_with(uuid=collect_request_uuid_fixture_1)


@mark.asyncio
async def test_search_wastes_by_ids_1() -> None:
    await collect_request_core._search_wastes_by_ids(wastes_ids=wastes_ids_fixture_1)
    calls = [
        call(uuid=wastes_ids_fixture_1[0]),
        call(uuid=wastes_ids_fixture_1[1]),
    ]
    collect_request_core.waste_provider.search_waste_by_id.assert_has_calls(calls)


@mark.asyncio
async def test_map_collect_response_1() -> None:
    request_create_response: CollectRequestCreateResponseDto = await collect_request_core._map_collect_response(collect_request_info=collect_request, wastes_info=wastes_list)
    assert request_create_response == request_create_response_fixture_1


@mark.asyncio
async def test_driver_create_request_1() -> None:
    collect_request_core.waste_provider.store_waste = MagicMock(side_effect=wastes_ids_fixture_1)
    collect_request_core.waste_provider.search_waste_by_id = MagicMock(side_effect=wastes_list)
    request_create_response: CollectRequestCreateResponseDto = await collect_request_core.driver_create_request(request_create_request=request_create_request_fixture_1)
    assert request_create_response == request_create_response_fixture_1
