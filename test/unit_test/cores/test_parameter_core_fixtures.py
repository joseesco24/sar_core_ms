# !/usr/bin/python3

# ** info: python imports
from os.path import join
from os import path
import sys

# ** info: typing imports
from typing import Set

# **info: appending src path to the system paths for absolute imports from src path
sys.path.append(join(path.dirname(path.realpath(__file__)), "..", "..", "..", "."))

# ** info: dtos imports
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos import ParameterSearchResponseDto  # type: ignore
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos import ParameterSearchRequestDto  # type: ignore
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos import ParameterDataDto  # type: ignore

# ** info: entities imports
from src.modules.parameter.adapters.database_providers_entities.parameter_entity import Parameter  # type: ignore

# ** info: sidecards.artifacts imports
from src.general_sidecards.artifacts.datetime_provider import DatetimeProvider  # type: ignore

# ---------------------------------------------------------------------------------------------------------------------
# ** info: create needed artifcts
# ---------------------------------------------------------------------------------------------------------------------

datetime_provider: DatetimeProvider = DatetimeProvider()

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
    order=1,
    create=datetime_provider.get_current_time(),
    update=datetime_provider.get_current_time(),
)

parameter_fixture_2: Parameter = Parameter(
    id=2,
    domain=r"wasteType",
    value=r"Combustible Nuclear",
    description=r"Residuos provenientes de reactores nucleares en los que se usa material nuclear para generar energía eléctrica",
    active=True,
    order=2,
    create=datetime_provider.get_current_time(),
    update=datetime_provider.get_current_time(),
)

parameter_list_fixture_1.append(parameter_fixture_1)
parameter_list_fixture_1.append(parameter_fixture_2)

paramaters_ids_fixture_1: Set[int] = set([parameter.id for parameter in parameter_list_fixture_1])


# ---------------------------------------------------------------------------------------------------------------------
# ** info: parameter search request dto fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

parameter_search_request_dto_fixture_1: ParameterSearchRequestDto = ParameterSearchRequestDto(domain=r"wasteType")

# ---------------------------------------------------------------------------------------------------------------------
# ** info: parameter search response dto fixtures declaration
# ---------------------------------------------------------------------------------------------------------------------

parameters_list_dto_fixture_1: list[ParameterDataDto] = list()

parameter_data_dto_fixture_1: ParameterDataDto = ParameterDataDto(label=parameter_list_fixture_1[0].value, value=parameter_list_fixture_1[0].id)

parameter_data_dto_fixture_2: ParameterDataDto = ParameterDataDto(label=parameter_list_fixture_1[1].value, value=parameter_list_fixture_1[1].id)

parameters_list_dto_fixture_1.append(parameter_data_dto_fixture_1)
parameters_list_dto_fixture_1.append(parameter_data_dto_fixture_2)

parameters_search_response_dto_fixture_1: ParameterSearchResponseDto = ParameterSearchResponseDto(values=parameters_list_dto_fixture_1)
