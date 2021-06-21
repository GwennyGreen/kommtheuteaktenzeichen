# pylint: disable=too-many-arguments, too-many-instance-attributes

"""Single episode of a series."""

from datetime import datetime, timezone, tzinfo
from typing import Any, Callable, Optional, TypedDict, Union, cast

from dateutil.relativedelta import relativedelta


class EpisodeDict(TypedDict):
    """Serialization structure for an Episode."""
    episodeNumber: Union[int, str]
    name: str
    datePublished: str
    sdDatePublished: str
    isRerun: bool
    isSpinoff: bool


class Episode:
    """Single episode of a series."""

    def __init__(self,
                 episode_number: Union[int, str],
                 name: str,
                 date_published: datetime,
                 sd_date_published: datetime,
                 is_rerun: bool = False,
                 is_spinoff: bool = False,
                 tz: Optional[tzinfo] = timezone.utc):
        self.episode_number: Union[int, str] = episode_number
        self.name: str = name
        self.date_published: datetime = \
            date_published.astimezone(timezone.utc)
        self.sd_date_published: datetime = \
            sd_date_published.astimezone(timezone.utc)
        self.is_rerun = is_rerun
        self.is_spinoff = is_spinoff
        self.timezone = tz

    def local_date_published(self) -> datetime:
        """Returns `date_published` in the local timezone."""
        return self.date_published.astimezone(self.timezone)

    def runs_today(
            self,
            now: Callable[..., datetime] = datetime.now
    ) -> bool:
        """
        Checks whether this episode’s `date_published` is on the
        same day as a given reference point in time, considering
        the timezone associated with this episode.

        Uses the current system time as a reference point, unless
        a Callable is given that produces a datetime.
        """
        return \
            self.date_published >= self.start_of_current_day(now) \
            and self.date_published < self.start_of_next_day(now)

    def runs_today_or_later(
            self,
            now: Callable[..., datetime] = datetime.now
    ) -> bool:
        """
        Checks whether this episode’s `date_published` is at least
        on the same day as a given reference point in time,
        considering the timezone associated with this episode.

        Uses the current system time as a reference point, unless
        a Callable is given that produces a datetime.
        """
        return \
            self.date_published >= self.start_of_current_day(now)

    def start_of_next_day(
        self,
        now: Callable[..., datetime] = datetime.now
    ) -> datetime:
        """
        Returns the start of the next day in the timezone
        associated with this episode. The resulting datetime is
        converted to UTC.
        Uses the current system time as a reference, unless
        a Callable is given that produces a datetime.
        """
        local_midnight = now().astimezone(self.timezone) \
            + relativedelta(days=+1,
                            hour=0, minute=0, second=0,
                            microsecond=0)
        return local_midnight.astimezone(timezone.utc)

    def start_of_current_day(
        self,
        now: Callable[..., datetime] = datetime.now
    ) -> datetime:
        """
        Returns the start of the current day in the timezone
        associated with this episode. The resulting datetime is
        converted to UTC.
        Uses the current system time as a reference, unless
        a Callable is given that produces a datetime.
        """
        return self.start_of_next_day(now=now) \
            + relativedelta(days=-1)

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if not isinstance(self, Episode):
            return False
        other_episode = cast(Episode, other)
        return (
            self.episode_number,
            self.is_rerun,
            self.is_spinoff,
        ) == (
            other_episode.episode_number,
            other_episode.is_rerun,
            other_episode.is_spinoff,
        )

    def __hash__(self) -> int:
        return (
            self.episode_number,
            self.is_rerun,
            self.is_spinoff,
        ).__hash__()
