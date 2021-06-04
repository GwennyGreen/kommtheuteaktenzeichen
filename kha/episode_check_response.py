"""Response to a request to check whether an episode runs today."""

from typing import Literal, TypedDict, Union

from .verdict import Verdict


class EpisodePresentResponse(TypedDict):
    """Response when an episode has been found."""
    verdict: Literal[Verdict.YES, Verdict.NO]
    reference_date: str
    start_date: str
    sd_date_published: str
    runs_today: bool
    episode_name: str
    episode_number: Union[int, str]


class EpisodeUnknownResponse(TypedDict):
    """Response when no episode has been found."""
    verdict: Literal[Verdict.UNKNOWN]


EpisodeCheckResponse = Union[
    EpisodePresentResponse, EpisodeUnknownResponse]
