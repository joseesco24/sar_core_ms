# !/usr/bin/python3
# type: ignore

# ** info: python imports
from calendar import month_name
from datetime import timedelta
from datetime import datetime
from datetime import UTC

# ** info: typing imports
from typing import Self


__all__: list[str] = ["DatetimeProvider"]


class DatetimeProvider:

    def get_month_literal(self: Self, month_number: int) -> str:
        return month_name[month_number].lower() if 1 <= month_number <= 12 else "undefined"

    def get_current_time(self: Self) -> datetime:
        return self.get_utc_time()

    def get_utc_time(self: Self) -> datetime:
        return datetime.now(UTC)

    def get_utc_pretty_string(self: Self) -> str:
        return self.prettify_date_time_obj(date_time_obj=self.get_utc_time())

    def iso_string_to_datetime(self: Self, iso_string: str) -> datetime:
        return datetime.strptime(iso_string, "%Y-%m-%d %H:%M:%S.%f")

    def pretty_date_string_to_date(self: Self, iso_string: str) -> datetime:
        return datetime.strptime(iso_string, "%d/%m/%Y")

    def get_utc_iso_string(self: Self) -> str:
        return self.get_utc_time().isoformat()

    def prettify_date_time_obj(self: Self, date_time_obj: datetime) -> str:
        return date_time_obj.strftime("%Y-%m-%d %H:%M:%S.%f")

    def prettify_date_obj(self: Self, date_time_obj: datetime) -> str:
        return date_time_obj.strftime("%d/%m/%Y")

    def prettify_time_delta_obj(self: Self, time_delta_obj: timedelta) -> str:
        delta_days: int = time_delta_obj.days
        delta_houres: int = time_delta_obj.seconds // 3600
        delta_minutes: int = time_delta_obj.seconds % 3600 // 60
        delta_seconds: int = time_delta_obj.seconds % 3600 % 60

        return f"{delta_days} days {delta_houres} houres {delta_minutes} minutes {delta_seconds} seconds"
