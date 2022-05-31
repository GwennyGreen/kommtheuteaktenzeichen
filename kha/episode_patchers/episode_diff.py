# pylint: disable=too-few-public-methods

"""Applies a change to an existing episode."""

from kha.episode import Episode
from kha.episode_patchers.noop_patcher import NoopPatcher
from kha.episode_patchers.patcher import Patcher
from kha.local_types import EventsDict


def episode_diff(events_dict: EventsDict,
                 incoming_episode: Episode) -> Patcher:
    return NoopPatcher()
