# !/usr/bin/python3
# type: ignore

# ** info: python imports
from datetime import datetime
import logging

# ** info: typing imports
from typing import Union
from typing import Self
from typing import Any

# ** info: sqlmodel imports
from sqlmodel import Session
from sqlmodel import select

# ** info: stamina imports
from stamina import retry

# ** info: fastapi imports
from fastapi import HTTPException
from fastapi import status

# ** info: users entity
from src.modules.waste.adapters.database_providers_entities.waste_entity import Waste

# ** info: sidecards.database_managers imports
from src.general_sidecards.database_managers.mysql_manager import MySQLManager

# ** info: sidecards.artifacts imports
from src.business_sidecards.constants.waste_states_constants import WasteStates
from src.general_sidecards.artifacts.datetime_provider import DatetimeProvider
from src.general_sidecards.artifacts.uuid_provider import UuidProvider
from src.general_sidecards.artifacts.env_provider import EnvProvider

# ** info: cachetools imports
from cachetools import TTLCache
from cachetools import cached

__all__: list[str] = ["WasteProvider"]

# ** info: creating a shared cache for all the waste provider instances
waste_provider_cache: TTLCache = TTLCache(ttl=240, maxsize=20)


class WasteProvider:
    def __init__(self: Self) -> None:
        self._env_provider: EnvProvider = EnvProvider()
        self._uuid_provider: UuidProvider = UuidProvider()
        self._datetime_provider: DatetimeProvider = DatetimeProvider()
        self._session_manager: MySQLManager = MySQLManager(
            password=self._env_provider.database_password,
            database=self._env_provider.database_name,
            username=self._env_provider.database_user,
            host=self._env_provider.database_host,
            port=self._env_provider.database_port,
            drivername=r"mysql+pymysql",
            query={"charset": "utf8"},
        )

    def clear_cache(self: Self) -> None:
        waste_provider_cache.clear()

    @cached(waste_provider_cache)
    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def search_waste_by_id(self: Self, uuid: str) -> Waste:
        logging.debug(f"searching waste by id {uuid}")
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Waste).where(Waste.uuid == uuid)
        search_waste_by_id_result: Waste = session.exec(statement=query).first()
        logging.debug("searching waste by id ended")
        return search_waste_by_id_result

    @cached(waste_provider_cache)
    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def list_wastes_by_process_status(self: Self, process_status: int) -> list[Waste]:
        logging.debug(f"searching wastes by process status {process_status}")
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Waste).where(Waste.process_status == process_status)
        search_waste_by_domain_result: list[Waste] = session.exec(statement=query).all()
        logging.debug("searching wastes by process status ended")
        return search_waste_by_domain_result

    @cached(waste_provider_cache)
    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def list_wastes_by_collect_request_id(self: Self, collect_request_uuid: str) -> list[Waste]:
        logging.debug(f"searching wastes by collect request id {collect_request_uuid}")
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Waste).where(Waste.request_uuid == collect_request_uuid)
        list_wastes_by_collect_request_id: list[Waste] = session.exec(statement=query).all()
        logging.debug("searching wastes by collect request id ended")
        return list_wastes_by_collect_request_id

    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def create_waste_with_basic_info(
        self: Self,
        request_uuid: str,
        type: int,
        packaging: int,
        weight_in_kg: float,
        volume_in_l: float,
        description: str,
        note: Union[str, None] = None,
    ) -> Waste:
        logging.debug("creating new waste with basic info")
        session: Session = self._session_manager.obtain_session()
        uuid: str = self._uuid_provider.get_str_uuid()
        date_time: datetime = self._datetime_provider.get_current_time()
        new_waste: Waste = Waste(
            uuid=uuid,
            request_uuid=request_uuid,
            type=type,
            packaging=packaging,
            process_status=WasteStates.in_review,
            weight_in_kg=weight_in_kg,
            volume_in_l=volume_in_l,
            description=description,
            note=note,
            create=date_time,
            update=date_time,
        )
        session.add(new_waste)
        session.commit()
        session.refresh(new_waste)
        self.clear_cache()
        logging.debug("new waste with basic info created")
        return new_waste

    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def update_waste_internal_classification_info(self: Self, uuid: str, isotopes_number: float, state_waste: int, store: int) -> Waste:
        logging.debug(f"updating waste {uuid} internal classification info")
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Waste).where(Waste.uuid == uuid)
        waste_data: Waste = session.exec(statement=query).first()
        if waste_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="waste not found")
        waste_data.update = self._datetime_provider.get_current_time()
        waste_data.process_status = WasteStates.waste_treatement_in_course
        waste_data.isotopes_number = isotopes_number
        waste_data.state_waste = state_waste
        waste_data.store = store
        session.add(waste_data)
        session.commit()
        session.refresh(waste_data)
        self.clear_cache()
        logging.debug(f"waste {uuid} internal classification info updated")
        return waste_data

    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def update_waste_status(self: Self, uuid: str, process_status: int) -> Waste:
        logging.debug(f"updating waste {uuid} status")
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Waste).where(Waste.uuid == uuid)
        waste_data: Waste = session.exec(statement=query).first()
        if waste_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="waste not found")
        waste_data.update = self._datetime_provider.get_current_time()
        waste_data.process_status = process_status
        session.add(waste_data)
        session.commit()
        session.refresh(waste_data)
        self.clear_cache()
        logging.debug(f"waste {uuid} status updated")
        return waste_data

    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def update_waste_status_by_request_id(self: Self, request_uuid: str, process_status: int) -> list[Waste]:
        logging.debug(f"updating waste {request_uuid} status")
        return_wastes: list[Waste] = []
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Waste).where(Waste.request_uuid == request_uuid)
        wastes: list[Waste] = session.exec(statement=query).all()
        if wastes is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wastes not found")
        for waste in wastes:
            waste.update = self._datetime_provider.get_current_time()
            waste.process_status = process_status
            session.add(waste)
        session.commit()
        for waste in wastes:
            session.refresh(waste)
            return_wastes.append(waste)
        self.clear_cache()
        logging.debug(f"waste {request_uuid} status updated")
        return return_wastes

    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def update_waste_status_and_store_id_by_request_id(self: Self, request_uuid: str, process_status: int, store_id: int) -> list[Waste]:
        logging.debug(f"updating waste {request_uuid} status")
        return_wastes: list[Waste] = []
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Waste).where(Waste.request_uuid == request_uuid)
        wastes: list[Waste] = session.exec(statement=query).all()
        if wastes is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wastes not found")
        for waste in wastes:
            waste.update = self._datetime_provider.get_current_time()
            waste.process_status = process_status
            waste.store = store_id
            session.add(waste)
        session.commit()
        for waste in wastes:
            session.refresh(waste)
            return_wastes.append(waste)
        self.clear_cache()
        logging.debug(f"waste {request_uuid} status updated")
        return return_wastes

    @cached(waste_provider_cache)
    @retry(on=Exception, attempts=4, wait_initial=0.08, wait_exp_base=2)
    def search_wastes_by_ids(self: Self, uuids: tuple[str, ...]) -> list[Waste]:
        logging.debug(f"searching wastes by ids {", ".join(uuids)}")
        session: Session = self._session_manager.obtain_session()
        query: Any = select(Waste).where(Waste.uuid.in_(uuids))
        search_waste_by_id_result: list[Waste] = session.exec(statement=query).all()
        logging.debug("searching wastes by ids ended")
        return search_waste_by_id_result
