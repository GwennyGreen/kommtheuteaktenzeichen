# pylint: disable=missing-function-docstring, missing-module-docstring

from collections.abc import Callable
from datetime import datetime, timezone, tzinfo
from typing import Any
from zoneinfo import ZoneInfo

import pytest


@pytest.fixture(name='local_timezone')
def fixture_local_timezone() -> tzinfo:
    local_timezone = ZoneInfo('Europe/Berlin')
    assert local_timezone is not None
    return local_timezone


@pytest.fixture(name='now')
def fixture_now() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2021-05-30T14:17:35+02:00')


@pytest.fixture(name='right_before_the_episode_starts')
def fixture_right_before_the_episode_starts() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2021-06-09T20:14:44+02:00')


@pytest.fixture(name='when_the_episode_starts')
def fixture_when_the_episode_starts() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2021-06-09T20:15:00+02:00')


@pytest.fixture(name='while_episode_is_running')
def fixture_while_episode_is_running() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2021-06-09T21:00:00+02:00')


@pytest.fixture(name='a_bit_past_midnight')
def fixture_a_bit_past_midnight() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2021-06-10T00:25:37+02:00')


@pytest.fixture(name='episode_boilerplate')
def fixture_episode_boilerplate(
    now: Callable[[], datetime],
    when_the_episode_starts: Callable[[], datetime],
    local_timezone: tzinfo,
) -> dict[str, Any]:
    return {
        'date_published': when_the_episode_starts()
        .astimezone(timezone.utc),
        'sd_date_published': now()
        .astimezone(timezone.utc),
        'is_rerun': False,
        'is_spinoff': False,
        'timezone': local_timezone,
    }
