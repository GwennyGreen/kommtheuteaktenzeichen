# pylint: disable=too-few-public-methods

"""Response to a request to check whether an episode runs today."""

from typing import Literal, Union

from .local_types import IsoDatetimeStr
from .verdict import Verdict


class EpisodePresentResponse:
    """Response when an episode has been found."""

    def __init__(self,  # pylint: disable=too-many-arguments
                 verdict: Literal[Verdict.YES, Verdict.NO],
                 reference_date: IsoDatetimeStr,
                 start_date: IsoDatetimeStr,
                 sd_date_published: IsoDatetimeStr,
                 runs_today: bool,
                 episode_name: str,
                 episode_number: Union[int, str]):
        self.verdict = verdict
        self.reference_date = reference_date
        self.start_date = start_date
        self.sd_date_published = sd_date_published
        self.runs_today = runs_today
        self.episode_name = episode_name
        self.episode_number = episode_number


class EpisodeUnknownResponse:
    """Response when no episode has been found."""

    def __init__(self, sd_date_published: IsoDatetimeStr):
        self.verdict: Literal[Verdict.UNKNOWN] = Verdict.UNKNOWN
        self.sd_date_published = sd_date_published


EpisodeCheckResponse = Union[
    EpisodePresentResponse, EpisodeUnknownResponse]
