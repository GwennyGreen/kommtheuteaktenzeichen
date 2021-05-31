"""Single episode of a series."""

from datetime import datetime, timezone, tzinfo
from typing import Callable, Optional, TypedDict, Union

from dateutil.relativedelta import relativedelta


class EpisodeDict(TypedDict):
    """Serialization structure for an Episode."""
    episodeNumber: Union[int, str]
    name: str
    datePublished: str
    sdDatePublished: str


class Episode:
    """Single episode of a series."""

    def __init__(self, source_dict: EpisodeDict,
                 tz: Optional[tzinfo] = timezone.utc):
        self.episode_number: Union[int, str] \
            = source_dict['episodeNumber']
        self.name: str \
            = source_dict['name']
        self.date_published: datetime \
            = datetime \
            .fromisoformat(source_dict['datePublished']) \
            .astimezone(timezone.utc)
        self.sd_date_published: datetime \
            = datetime \
            .fromisoformat(source_dict['sdDatePublished']) \
            .astimezone(timezone.utc)
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
