"""Package-scoped type annotations."""

from typing import Dict, NewType, TypedDict

from episode import Episode


Uuid = NewType('Uuid', str)


class EpisodesDict(TypedDict):
    """Dictionary of episodes, addressable by ID."""
    episodes: Dict[Uuid, Episode]


class EventsDict(TypedDict):
    """Top-level dictionary."""
    episodes: EpisodesDict
