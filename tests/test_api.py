# pylint: disable=missing-function-docstring, missing-module-docstring

from collections.abc import Callable, Iterable
from datetime import datetime, timezone
from typing import Any

import pytest

from kha import api
from kha.episode import Episode


@pytest.fixture(name='episode_566')
def fixture_episode_566(
    episode_boilerplate: dict[str, Any]
) -> Episode:
    return Episode(
        566,
        name='Folge 566',
        **(episode_boilerplate | {  # type: ignore
            'date_published': datetime
            .fromisoformat('2021-05-12T20:15:00+02:00')
            .astimezone(timezone.utc)
        }),
    )


@pytest.fixture(name='episode_567')
def fixture_episode_567(
    episode_boilerplate: dict[str, Any]
) -> Episode:
    return Episode(
        567,
        name='Folge 567',
        **episode_boilerplate,
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
