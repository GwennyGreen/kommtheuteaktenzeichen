# pylint: disable=missing-function-docstring, missing-module-docstring

from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

import pytest

from kha.episode import Episode


@pytest.fixture(name='episode_in_utc')
def fixture_episode_in_utc(
    episode_boilerplate: dict[str, Any],
) -> Episode:
    return Episode(
        567,
        name='Folge 567',
        **(episode_boilerplate | {  # type: ignore
            'timezone': timezone.utc,
        }),
    )


@pytest.fixture(name='episode_in_local_timezone')
def fixture_episode_in_local_timezone(
    episode_boilerplate: dict[str, Any],
) -> Episode:
    return Episode(
        567,
        name='Folge 567',
        **episode_boilerplate,
    )


@pytest.fixture(name='rerun_episode')
def fixture_rerun_episode(
    episode_boilerplate: dict[str, Any],
) -> Episode:
    return Episode(
        567,
        name='Folge 567',
        **(episode_boilerplate | {  # type: ignore
            'is_rerun': True,
        }),
    )


def test_types(episode_in_utc: Episode) -> None:
    assert isinstance(episode_in_utc.date_published, datetime)
    assert isinstance(episode_in_utc.sd_date_published, datetime)


def test_utc_date_published(episode_in_utc: Episode) -> None:
    assert episode_in_utc \
        .local_date_published() \
        .isoformat(timespec='seconds') \
        == '2021-06-09T18:15:00+00:00'


def test_local_date_published(
        episode_in_local_timezone: Episode) -> None:
    assert episode_in_local_timezone \
        .local_date_published() \
        .isoformat(timespec='seconds') \
        == '2021-06-09T20:15:00+02:00'


def test_start_of_next_day(episode_in_local_timezone: Episode,
                           now: Callable[[], datetime]) -> None:
    assert episode_in_local_timezone.start_of_next_day(now=now) \
        .isoformat(timespec='seconds') \
        == '2021-05-30T22:00:00+00:00'


def test_start_of_current_day(episode_in_local_timezone: Episode,
                              now: Callable[[], datetime]) -> None:
    assert episode_in_local_timezone.start_of_current_day(now=now) \
        .isoformat(timespec='seconds') \
        == '2021-05-29T22:00:00+00:00'


def test_upcoming_episode(
    now: Callable[[], datetime],
    episode_in_local_timezone: Episode,
) -> None:
    assert not episode_in_local_timezone.runs_today(now=now)
    assert episode_in_local_timezone.runs_today_or_later(now=now)


def test_runs_today_start_has_not_passed(
    right_before_the_episode_starts: Callable[[], datetime],
    episode_in_local_timezone: Episode,
) -> None:
    assert episode_in_local_timezone.runs_today(
        now=right_before_the_episode_starts)
    assert episode_in_local_timezone.runs_today_or_later(
        now=right_before_the_episode_starts)


def test_runs_today_start_has_passed(
    while_episode_is_running: Callable[[], datetime],
    episode_in_local_timezone: Episode,
) -> None:
    assert episode_in_local_timezone.runs_today(
        now=while_episode_is_running)
    assert episode_in_local_timezone.runs_today_or_later(
        now=while_episode_is_running)


def test_past_episode(
    a_bit_past_midnight: Callable[[], datetime],
    episode_in_local_timezone: Episode,
) -> None:
    assert not episode_in_local_timezone.runs_today(
        now=a_bit_past_midnight)
    assert not episode_in_local_timezone.runs_today_or_later(
        now=a_bit_past_midnight)


def test_domain_key(
    episode_in_utc: Episode,
    episode_in_local_timezone: Episode,
    rerun_episode: Episode,
) -> None:
    assert episode_in_utc.domain_key \
        == episode_in_local_timezone.domain_key
    assert episode_in_local_timezone.domain_key \
        != rerun_episode.domain_key
