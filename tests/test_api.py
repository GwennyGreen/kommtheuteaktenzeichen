# pylint: disable=missing-function-docstring, missing-module-docstring

from collections.abc import Iterable
from datetime import datetime, timezone, tzinfo
from typing import Callable
from zoneinfo import ZoneInfo

import pytest

from kha import api
from kha.episode import Episode


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


@pytest.fixture(name='local_timezone')
def fixture_local_timezone() -> tzinfo:
    local_timezone = ZoneInfo('Europe/Berlin')
    assert local_timezone is not None
    return local_timezone


@pytest.fixture(name='episode_566')
def fixture_episode_566(
        now: Callable[[], datetime],
        local_timezone: tzinfo,
) -> Episode:
    return Episode(
        566,
        name='Folge 566',
        date_published=datetime
        .fromisoformat('2021-05-12T20:15:00+02:00')
        .astimezone(timezone.utc),
        sd_date_published=now()
        .astimezone(timezone.utc),
        is_rerun=False,
        is_spinoff=False,
        timezone=local_timezone,
    )


@pytest.fixture(name='episode_567')
def fixture_episode_567(
        now: Callable[[], datetime],
        when_the_episode_starts: Callable[[], datetime],
        local_timezone: tzinfo,
) -> Episode:
    return Episode(
        567,
        name='Folge 567',
        date_published=when_the_episode_starts()
        .astimezone(timezone.utc),
        sd_date_published=now()
        .astimezone(timezone.utc),
        is_rerun=False,
        is_spinoff=False,
        timezone=local_timezone,
    )


@pytest.fixture(name='episodes')
def fixture_episodes(episode_566: Episode, episode_567: Episode) \
        -> Iterable[Episode]:
    return [episode_567, episode_566]


def test_next_start(episodes: Iterable[Episode],
                    now: Callable[[], datetime]) -> None:
    episode = api.next_episode(episodes=episodes, after=now)
    assert episode is not None
    assert episode \
        .local_date_published() \
        .isoformat(timespec='seconds') \
        == '2021-06-09T20:15:00+02:00'


def test_start_has_not_passed(episodes: Iterable[Episode],
                              right_before_the_episode_starts: Callable[[], datetime]) \
        -> None:
    episode = api.next_episode(episodes=episodes,
                               after=right_before_the_episode_starts)
    assert episode is not None
    assert episode \
        .local_date_published() \
        .isoformat(timespec='seconds') \
        == '2021-06-09T20:15:00+02:00'


def test_start_has_passed(episodes: Iterable[Episode],
                          while_episode_is_running: Callable[[], datetime]) -> None:
    episode = api.next_episode(episodes=episodes,
                               after=while_episode_is_running)
    assert episode is not None
    assert episode \
        .local_date_published() \
        .isoformat(timespec='seconds') \
        == '2021-06-09T20:15:00+02:00'


def test_no_upcoming_episodes(episodes: Iterable[Episode],
                              a_bit_past_midnight: Callable[[], datetime]) -> None:
    episode = api.next_episode(episodes=episodes,
                               after=a_bit_past_midnight)
    assert episode is None
