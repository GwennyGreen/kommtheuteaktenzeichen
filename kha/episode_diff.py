from kha.episode import Episode
from kha.episode_patchers.episode_adder import EpisodeAdder
from kha.episode_patchers.episode_replacer import EpisodeReplacer
from kha.episode_patchers.noop_patcher import NoopPatcher
from kha.episode_patchers.patcher import Patcher
from kha.local_types import EventsDict, Uuid


def episode_diff(events_dict: EventsDict,
                 incoming_episode: Episode) -> Patcher:
    return NoopPatcher()
