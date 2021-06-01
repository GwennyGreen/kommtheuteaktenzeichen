"""API entry point of the kha package."""
from datetime import datetime
import json
import operator
import re
import textwrap
from typing import Any, Callable, Dict, Iterable, Optional, Union, cast

import dateutil.tz

import settings  # type: ignore
from episode import Episode, EpisodeDict
from episode_check_response import EpisodeCheckResponse, \
    EpisodePresentResponse, EpisodeUnknownResponse
from local_types import EventsDict
from verdict import Verdict

USER_TIMEZONE = dateutil.tz.gettz('Europe/Berlin')
ZDF_DATE_SEARCH_PATTERN = \
    r'Nächste Sendung: (?P<next_date>\d{2}\.\d{2}\.\d{4})'
ZDF_DATE_FORMAT = r'%d.%m.%Y'
ZDF_IMPLIED_TIMEZONE = dateutil.tz.gettz('Europe/Berlin')

EVENTS_JSON_PATH = \
    settings.PROJECT_ROOT / 'etc' / 'events.kha.json'


def check_episode() -> str:
    """Kommt heute Aktenzeichen?"""
    print(textwrap.dedent(
        """\
        Kommt heute Aktenzeichen?
        """
    ))
    check_response = check()
    print({
        Verdict.YES: 'Ja.',
        Verdict.NO: 'Nein.',
        Verdict.UNKNOWN: 'Keine Ahnung.',
    }[check_response['verdict']])
    return json.dumps(check_response, indent=2)


def check(
    episodes: Optional[Iterable[Episode]] = None,
    now: Callable[..., datetime] = datetime.now,
) -> EpisodeCheckResponse:
    """
    Checks whether an episode runs today. What today means
    is derived from a given point in time, the *reference point*.

    Uses the current system time as a reference point, unless
    a Callable is given that produces a datetime.
    An episode is considered to *run today* if its start date is
    on the same day as the reference point, considering the user’s
    assumed timezone of `Europe/Berlin`.

    This function uses the episode list in `events.kha.json`,
    unless `episodes` is given.
    """
    episode = next_episode(episodes=episodes, after=now)
    if episode is None:
        return EpisodeUnknownResponse({
            'verdict': Verdict.UNKNOWN
        })

    return EpisodePresentResponse({
        'verdict':
        Verdict.YES if episode.runs_today() else Verdict.NO,
        'reference_date':
        now().astimezone(USER_TIMEZONE)
            .isoformat(timespec='seconds'),
        'start_date':
        episode.date_published.astimezone(USER_TIMEZONE)
            .isoformat(timespec='seconds'),
        'runs_today': episode.runs_today(),
        'episode_name': episode.name,
        'episode_number': episode.episode_number,
    })


def next_episode(
    episodes: Optional[Iterable[Episode]] = None,
    after: Callable[..., datetime] = datetime.now,
) -> Optional[Episode]:
    """
    Returns the current or next episode that is broadcast
    relative to a given point in time, the *reference point*.
    Returns None if no such episode can be found.

    Uses the current system time as a reference point, unless
    a Callable is given that produces a datetime.
    An episode is considered current as long as its start date is
    at least on the same day as the reference point. In other words,
    the episode is still current if the reference point is past the
    broadcast time (but not past midnight).

    This function uses the episode list in `events.kha.json`,
    unless `episodes` is given.
    """
    filtered_sorted_episodes = sorted(
        [
            episode
            for episode
            in (episodes if episodes else cast(
                Iterable[Episode],
                _events_dict_from_file()['episodes'].values())
                )
            if episode.runs_today_or_later(now=after)
        ],
        key=operator.attrgetter('date_published')
    )

    if not filtered_sorted_episodes:
        return None
    return next(iter(filtered_sorted_episodes))


def _events_dict_from_file() -> EventsDict:
    """
    Loads an EventsDict from a file and returns it, sorted by
    start date.
    """
    def deserialize(obj: Dict[str, Any]) \
            -> Union[Dict[str, Any], Episode]:
        if '@type' in obj:
            if obj['@type'] == 'Episode':
                return Episode(cast(EpisodeDict, obj),
                               tz=USER_TIMEZONE)
            raise RuntimeError(f'Unknown type `{obj["@type"]}`')
        return obj

    with EVENTS_JSON_PATH.open(encoding='UTF-8') as events_json:
        return cast(
            EventsDict,
            json.load(events_json,
                      object_hook=deserialize)
        )


def parse_zdf_datetime(html_source: str) -> datetime:
    """Parses a datetime from the ZDF website."""
    next_date_strings = set(re.findall(
        ZDF_DATE_SEARCH_PATTERN,
        html_source
    ))
    if not next_date_strings:
        raise RuntimeError('Unable to find date on zdf.de')
    if len(next_date_strings) > 1:
        raise RuntimeError(
            f'Found ambiguous dates {",".join(next_date_strings)} '
            + 'on zdf.de'
        )

    next_date = datetime.strptime(
        next(iter(next_date_strings)),
        ZDF_DATE_FORMAT
    )

    return datetime(
        next_date.year,
        next_date.month,
        next_date.day,
        20,
        15,
        00,
        tzinfo=ZDF_IMPLIED_TIMEZONE
    ).astimezone(dateutil.tz.UTC)
