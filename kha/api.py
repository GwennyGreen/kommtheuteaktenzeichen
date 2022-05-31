"""API entry point of the kha package."""

from datetime import datetime, timezone
import json
import operator
import os
from typing import Any, Callable, Dict, Iterable, List, Optional, Union, cast

import boto3
from mypy_boto3_s3.client import S3Client

from .episode import Episode, EpisodeDict
from .episode_check_response import EpisodeCheckResponse, \
    EpisodePresentResponse, EpisodeUnknownResponse
from .local_types import EventsDict, IsoDatetimeStr
from .settings \
    import EVENTS_JSON_BUCKET_DEV, EVENTS_JSON_BUCKET_PROD, \
    EVENTS_JSON_FILENAME, LOCAL_EVENTS_JSON_PATH, USER_TIMEZONE
from .verdict import Verdict


def check_episode() -> str:
    """Kommt heute Aktenzeichen?"""
    print('Kommt heute Aktenzeichen?')
    check_response = check()
    print({
        Verdict.YES: 'Ja.',
        Verdict.NO: 'Nein.',
        Verdict.UNKNOWN: 'Keine Ahnung.',
    }[check_response.verdict])
    return json.dumps(check_response.__dict__, indent=2)


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
        return EpisodeUnknownResponse(
            sd_date_published=IsoDatetimeStr(
                now()
                .astimezone(USER_TIMEZONE)
                .isoformat(timespec='seconds')
            )
        )

    return EpisodePresentResponse(
        verdict=Verdict.YES if episode.runs_today() else Verdict.NO,
        reference_date=IsoDatetimeStr(
            now()
            .astimezone(USER_TIMEZONE)
            .isoformat(timespec='seconds')
        ),
        start_date=IsoDatetimeStr(
            episode.date_published
            .astimezone(USER_TIMEZONE)
            .isoformat(timespec='seconds')
        ),
        sd_date_published=IsoDatetimeStr(
            now()
            .astimezone(USER_TIMEZONE)
            .isoformat(timespec='seconds')
        ),
        runs_today=episode.runs_today(),
        episode_name=episode.name,
        episode_number=episode.episode_number,
    )


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
    unfiltered_episodes = episodes if episodes \
        else all_episodes_from_store()

    filtered_sorted_episodes = sorted(
        [
            episode
            for episode
            in filter_eligible_episodes(unfiltered_episodes)
            if episode.runs_today_or_later(now=after)
        ],
        key=operator.attrgetter('date_published'),
    )

    if not filtered_sorted_episodes:
        return None
    return next(iter(filtered_sorted_episodes))


def _merge(
    episodes: Iterable[Episode],
    new_episodes: Iterable[Episode],
) -> List[Episode]:
    """
    Merges existing and new episodes together.
    Returns a list, sorted by start date.
    """
    return sorted(
        list(set(episodes) | set(new_episodes)),
        key=operator.attrgetter('date_published'),
    )


def filter_eligible_episodes(
        unfiltered_episodes: Iterable[Episode]) \
        -> Iterable[Episode]:
    """
    From a given list of unfiltered episodes, return eligible
    episodes. An episode is eligible if and only if:
    1. it is not a rerun;
    2. it is not a spinoff, or it is followed only by spinoffs.
    Returns a list, sorted by start date.
    """
    def last_published_date_ignoring_spinoffs() \
            -> Optional[datetime]:
        """
        Of all start dates of known episodes, return the latest one,
        ignoring spin-off episodes.
        Return None if no such episode exists.
        """
        start_dates = [
            episode.date_published
            for episode in unfiltered_episodes
            if not(episode.is_rerun or episode.is_spinoff)
        ]
        if not start_dates:
            return None
        return max(start_dates)

    pivot_date = last_published_date_ignoring_spinoffs()
    spinoff_episodes_wanted = not pivot_date

    for episode in unfiltered_episodes:
        if episode.is_rerun:
            continue
        if pivot_date and episode.date_published >= pivot_date:
            spinoff_episodes_wanted = True
        if spinoff_episodes_wanted or not episode.is_spinoff:
            yield episode


def all_episodes_from_store(client: Optional[S3Client] = None) \
        -> List[Episode]:
    """
    Loads all episodes from the backing store and returns them,
    sorted by start date.
    """
    return sorted(
        cast(Iterable[Episode],
             events_dict_from_store(client)['episodes'].values()),
        key=operator.attrgetter('date_published'),
    )


def _deserialize_events_dict(obj: Dict[str, Any]) \
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
                timezone=USER_TIMEZONE,
            )
        raise RuntimeError(f'Unknown type `{obj["@type"]}`')
    return obj


def _events_dict_from_file() -> EventsDict:
    """
    Loads an EventsDict from a file and returns it, sorted by
    start date.
    """
    with LOCAL_EVENTS_JSON_PATH.open(encoding='UTF-8') \
            as events_json:
        return cast(
            EventsDict,
            json.load(events_json,
                      object_hook=_deserialize_events_dict)
        )


def events_dict_from_store(client: Optional[S3Client] = None) -> EventsDict:
    """
    Loads an EventsDict from the backing store and returns it,
    sorted by start date.
    """
    s3_client = client or boto3.client('s3')
    response = s3_client.get_object(
        Bucket=os.environ['KHA_DATA_S3_BUCKET'],
        Key=EVENTS_JSON_FILENAME
    )
    return cast(
        EventsDict,
        json.load(response['Body'],
                  object_hook=_deserialize_events_dict)
    )


def list_eligible_episodes(client: Optional[S3Client] = None) \
        -> None:
    """
    From all known episodes in the backing store, prints a list of
    eligible episodes. An episode is eligible if and only if:
    1. it is not a rerun;
    2. it is not a spinoff, or it is followed only by spinoffs.
    """
    for episode \
            in filter_eligible_episodes(
                all_episodes_from_store(client)):
        print(repr(episode))


def print_episodes_dev(client: Optional[S3Client] = None) -> None:
    """
    Downloads episodes from the backing store and prints them
    on standard output.
    """
    _print_episodes(EVENTS_JSON_BUCKET_DEV, client)


def print_episodes_prod(client: Optional[S3Client] = None) -> None:
    """
    Downloads episodes from the backing store and prints them
    on standard output.
    """
    _print_episodes(EVENTS_JSON_BUCKET_PROD, client)


def _print_episodes(bucket: str,
                    client: Optional[S3Client] = None) -> None:
    s3_client = client or boto3.client('s3')
    response = s3_client.get_object(
        Bucket=bucket,
        Key=EVENTS_JSON_FILENAME,
    )
    print(response['Body'].read().decode())
