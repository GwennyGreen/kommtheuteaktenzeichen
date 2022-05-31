# pylint: disable=missing-function-docstring, missing-module-docstring, no-self-use

from datetime import datetime

import pytest

from kha.episode import Episode
from kha.episode_patchers.episode_diff import episode_diff
from kha.episode_patchers.noop_patcher import NoopPatcher
from kha.local_types import EventsDict, Uuid


@pytest.fixture(name='episode_566_original')
def fixture_episode_566_original() -> Episode:
    return Episode(
        566,
        name='Folge 566',
        date_published=datetime.fromisoformat(
            '2021-05-12T20:15:00+02:00'),
        sd_date_published=datetime.fromisoformat(
            '2021-05-30T16:37:17+02:00'),
    )


@pytest.fixture(name='episode_567_original')
def fixture_episode_567_original() -> Episode:
    return Episode(
        567,
        name='Folge 567',
        date_published=datetime.fromisoformat(
            '2021-06-09T20:15:00+02:00'),
        sd_date_published=datetime.fromisoformat(
            '2021-05-30T12:19:06+02:00'),
    )


@pytest.fixture(name='episode_568_original')
def fixture_episode_568_original() -> Episode:
    return Episode(
        568,
        name='Folge 568',
        date_published=datetime.fromisoformat(
            '2021-07-14T20:15:00+02:00'),
        sd_date_published=datetime.fromisoformat(
            '2021-06-07T23:01:34+02:00'),
    )


@pytest.fixture(name='dict_with_three_events')
def fixture_dict_with_three_events(
    episode_566_original: Episode,
    episode_567_original: Episode,
    episode_568_original: Episode,
) -> EventsDict:
    return EventsDict({
        'episodes': {
            Uuid('A9EDED35-CDFE-4E45-9D75-2BE3B68499F6'):
            episode_567_original,
            Uuid('EA223330-2DB3-4C6F-89CA-9B6A862AFAB4'):
            episode_566_original,
            Uuid('EDDA358F-5981-4C0D-9122-94E753EC37D8'):
            episode_568_original,
        },
    })


def test_replace_566_with_itself(
    dict_with_three_events: EventsDict,
    episode_566_original: Episode,
) -> None:
    patcher = episode_diff(dict_with_three_events,
                           episode_566_original)
    assert isinstance(patcher, NoopPatcher)


def test_replace_567_with_itself(
    dict_with_three_events: EventsDict,
    episode_567_original: Episode,
) -> None:
    patcher = episode_diff(dict_with_three_events,
                           episode_567_original)
    assert isinstance(patcher, NoopPatcher)


def test_replace_568_with_itself(
    dict_with_three_events: EventsDict,
    episode_568_original: Episode,
) -> None:
    patcher = episode_diff(dict_with_three_events,
                           episode_568_original)
    assert isinstance(patcher, NoopPatcher)
