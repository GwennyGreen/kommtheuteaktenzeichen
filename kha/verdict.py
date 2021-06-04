"""Verdict of an `EpisodeCheckResponse`."""

from enum import IntEnum

class Verdict(IntEnum):
    """Verdict of an `EpisodeCheckResponse`."""
    YES = 0
    NO = 1
    UNKNOWN = 2
