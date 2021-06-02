"""API entry point of the kha package."""

from datetime import datetime, timezone
import json
import operator
import textwrap
from typing import Any, Callable, Dict, Iterable, Optional, Union, cast

import dateutil.tz

from episode import Episode, EpisodeDict
from episode_check_response import EpisodeCheckResponse, \
    EpisodePresentResponse, EpisodeUnknownResponse
from local_types import EventsDict
import parse
import settings  # type: ignore
from verdict import Verdict

USER_TIMEZONE = dateutil.tz.gettz('Europe/Berlin')

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

    This function uses the given episode list. If none is given,
    it loads episodes from the file `events.kha.json`, merges it
    with episodes found online and uses the result.
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

    This function uses the given episode list. If none is given,
    it loads episodes from the file `events.kha.json`, merges it
    with episodes found online and uses the result.
    """
    filtered_sorted_episodes = sorted(
        [
            episode
            for episode
            in (episodes if episodes else all_episodes())
            if episode.runs_today_or_later(now=after)
        ],
        key=operator.attrgetter('date_published'),
    )

    if not filtered_sorted_episodes:
        return None
    return next(iter(filtered_sorted_episodes))


def _merge(episodes, new_episodes):
    """
    Merges existing and new episodes together.
    Returns a list, sorted by start date.
    """
    return sorted(
        list(set(episodes) | set(new_episodes)),
        key=operator.attrgetter('date_published'),
    )


def all_episodes() -> Iterable[Episode]:
    """
    Loads all known episodes from a file and merges them with
    the episodes found online.
    Returns a list, sorted by start date.
    """
    return (
        episode
        for episode in _merge(
            all_episodes_from_file(),
            parse.parse_wunschliste(),
        )
        if not(episode.is_rerun or episode.is_spinoff)
    )


def all_episodes_from_file() -> Iterable[Episode]:
    """
    Loads all episodes from a file and returns them, sorted by
    start date.
    """
    return sorted(
        cast(
            Iterable[Episode],
            _events_dict_from_file()['episodes'].values()),
        key=operator.attrgetter('date_published'),
    )


def _events_dict_from_file() -> EventsDict:
    """
    Loads an EventsDict from a file and returns it, sorted by
    start date.
    """
    def deserialize(obj: Dict[str, Any]) \
            -> Union[Dict[str, Any], Episode]:
        if '@type' in obj:
            if obj['@type'] == 'Episode':
                episode_dict = cast(EpisodeDict, obj)
                return Episode(
                    episode_dict['episodeNumber'],
                    name=episode_dict['name'],
                    date_published=datetime
                    .fromisoformat(episode_dict['datePublished'])
                    .astimezone(timezone.utc),
                    sd_date_published=datetime
                    .fromisoformat(episode_dict['sdDatePublished'])
                    .astimezone(timezone.utc),
                    is_rerun=episode_dict['isRerun'],
                    is_spinoff=episode_dict['isSpinoff'],
                    tz=USER_TIMEZONE,
                )
            raise RuntimeError(f'Unknown type `{obj["@type"]}`')
        return obj

    with EVENTS_JSON_PATH.open(encoding='UTF-8') as events_json:
        return cast(
            EventsDict,
            json.load(events_json,
                      object_hook=deserialize)
        )
