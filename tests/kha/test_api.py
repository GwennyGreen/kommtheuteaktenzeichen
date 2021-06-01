# pylint: disable=missing-function-docstring, missing-module-docstring, no-self-use

from datetime import datetime, timezone
from typing import Callable

import pytest

import api


@pytest.fixture(name='html_fragment_june')
def fixture_html_fragment_june() -> str:
    return '<p class="teaser-text">Nächste Sendung: 09.06.2021</p>'


@pytest.fixture(name='html_fragment_november')
def fixture_html_fragment_november() -> str:
    return '<p class="teaser-text">Nächste Sendung: 17.11.2021</p>'


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


def test_parse_cest_date(html_fragment_june: str) -> None:
    assert api \
        .parse_zdf_datetime(html_fragment_june) \
        == datetime(
            2021, 6, 9, 18, 15, tzinfo=timezone.utc)


def test_parse_cet_date(html_fragment_november: str) -> None:
    assert api \
        .parse_zdf_datetime(html_fragment_november) \
        == datetime(
            2021, 11, 17, 19, 15, tzinfo=timezone.utc)


def test_next_start(now: Callable[[], datetime]) -> None:
    episode = api.next_episode(after=now)
    assert episode is not None
    assert episode \
        .local_date_published() \
        .isoformat(timespec='seconds') \
        == '2021-06-09T20:15:00+02:00'


def test_start_has_not_passed(
    right_before_the_episode_starts: Callable[[], datetime]) \
        -> None:
    episode = api.next_episode(
        after=right_before_the_episode_starts)
    assert episode is not None
    assert episode \
        .local_date_published() \
        .isoformat(timespec='seconds') \
        == '2021-06-09T20:15:00+02:00'


def test_start_has_passed(
        while_episode_is_running: Callable[[], datetime]) -> None:
    episode = api.next_episode(
        after=while_episode_is_running)
    assert episode is not None
    assert episode \
        .local_date_published() \
        .isoformat(timespec='seconds') \
        == '2021-06-09T20:15:00+02:00'


def test_no_upcoming_episodes(
        a_bit_past_midnight: Callable[[], datetime]) -> None:
    episode = api.next_episode(
        after=a_bit_past_midnight)
    assert episode is None
