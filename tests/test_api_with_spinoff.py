# pylint: disable=missing-function-docstring, missing-module-docstring, no-self-use

from datetime import datetime, timezone, tzinfo
from typing import Callable, Iterable

import dateutil.tz
import pytest

from kha import api
from kha.episode import Episode


@pytest.fixture(name='before_episode_579')
def fixture_before_episode_579() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2022-05-31T22:00:00+02:00')


@pytest.fixture(name='after_episode_579')
def fixture_after_episode_579() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2022-06-02T08:00:00+02:00')


@pytest.fixture(name='after_episode_spinoff_1')
def fixture_after_episode_spinoff_1() -> Callable[[], datetime]:
    return lambda: datetime.fromisoformat(
        '2022-06-30T08:00:00+02:00')


@pytest.fixture(name='local_timezone')
def fixture_local_timezone() -> tzinfo:
    local_timezone = dateutil.tz.gettz('Europe/Berlin')
    assert local_timezone is not None
    return local_timezone


@pytest.fixture(name='episode_579')
def fixture_episode_579(
        local_timezone: tzinfo,
) -> Episode:
    return Episode(
        579,
        name='Folge 579',
        date_published=datetime
        .fromisoformat('2022-06-01T20:15:00+02:00')
        .astimezone(timezone.utc),
        sd_date_published=datetime
        .fromisoformat('2021-12-18T07:16:07+00:00')
        .astimezone(timezone.utc),
        is_rerun=False,
        is_spinoff=True,
        timezone=local_timezone
    )


@pytest.fixture(name='episode_spinoff_1')
def fixture_episode_spinoff_1(
        local_timezone: tzinfo,
) -> Episode:
    return Episode(
        1,
        name='Vermisst - Folge 1',
        date_published=datetime
        .fromisoformat('2022-06-29T20:15:00+02:00')
        .astimezone(timezone.utc),
        sd_date_published=datetime
        .fromisoformat('2022-05-23T00:19:48+02:00')
        .astimezone(timezone.utc),
        is_rerun=False,
        is_spinoff=True,
        timezone=local_timezone
    )


@pytest.fixture(name='episodes')
def fixture_episodes(episode_579: Episode, episode_spinoff_1: Episode) \
        -> Iterable[Episode]:
    return [episode_579, episode_spinoff_1]


def test_before_episode_579(
    episodes: Iterable[Episode],
    before_episode_579: Callable[[], datetime]
) -> None:
    episode = api.next_episode(episodes=episodes,
                               after=before_episode_579)
    assert episode is not None
    assert episode.episode_number == 579


def test_after_episode_579(
    episodes: Iterable[Episode],
    after_episode_579: Callable[[], datetime]
) -> None:
    episode = api.next_episode(episodes=episodes,
                               after=after_episode_579)
    assert episode is not None
    assert episode.episode_number == 1


def test_after_episode_spinoff_1(
    episodes: Iterable[Episode],
    after_episode_spinoff_1: Callable[[], datetime]
) -> None:
    episode = api.next_episode(episodes=episodes,
                               after=after_episode_spinoff_1)
    assert episode is None
