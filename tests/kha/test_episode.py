# pylint: disable=missing-function-docstring, missing-module-docstring, no-self-use

from datetime import datetime, tzinfo
from typing import Callable

import dateutil.tz
import pytest

from kha.episode import Episode, EpisodeDict


@pytest.fixture(name='episode_dict')
def fixture_episode_dict() -> EpisodeDict:
    return {
        'episodeNumber': 567,
        'name': 'Folge 567',
        'datePublished': '2021-06-09T20:15:00+02:00',
        'sdDatePublished': '2021-05-30T12:19:06+02:00'
    }


@pytest.fixture(name='local_timezone')
def fixture_local_timezone() -> tzinfo:
    local_timezone = dateutil.tz.gettz('Europe/Berlin')
    assert local_timezone is not None
    return local_timezone


@pytest.fixture(name='episode_in_local_timezone')
def fixture_episode_in_local_timezone(episode_dict,
                                      local_timezone) -> Episode:
    return Episode(episode_dict, tz=local_timezone)


@pytest.fixture(name='now')
def fixture_now() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2021-05-30T14:17:35+02:00')


@pytest.fixture(name='right_before_the_episode_starts')
def fixture_right_before_the_episode_starts() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2021-06-09T20:14:44+02:00')


@pytest.fixture(name='while_episode_is_running')
def fixture_while_episode_is_running() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2021-06-09T21:00:00+02:00')


@pytest.fixture(name='a_bit_past_midnight')
def fixture_a_bit_past_midnight() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2021-06-10T00:25:37+02:00')


def test_types(episode_dict: EpisodeDict) -> None:
    episode = Episode(episode_dict)
    assert isinstance(episode.date_published, datetime)
    assert isinstance(episode.sd_date_published, datetime)


def test_utc_date_published(episode_dict: EpisodeDict) -> None:
    episode = Episode(episode_dict)
    assert episode \
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
