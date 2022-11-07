"""Scrape episodes from online sources."""

from datetime import datetime
import re
from re import Match
from collections.abc import Iterable
from typing import Optional

import requests

from .episode import Episode
from .settings \
    import WUNSCHLISTE_IMPLIED_TIMEZONE, \
    WUNSCHLISTE_QUERY_PARAMETERS, WUNSCHLISTE_URL

WUNSCHLISTE_SELECT_EPISODE_PATTERN = r'(?ms)<li.*?</li>'

WUNSCHLISTE_PARSE_EPISODE_PATTERN = r"""(?msx)
    (?:
        heute|
        morgen|
        [A-Z][a-z],[^<]+              # Weekday
        (?P<day>\d{2})\.
        (?P<month>\d{2})\.
        <.*?>                         # Multiple text nodes or tags
        (?P<year>\d{4})
    )
    <.*?>                             # Multiple text nodes or tags
    (?P<hour>\d{1,2}):
    (?P<minute>\d{2})[^<]+h
    <.*?"Episode">                    # Multiple text nodes or tags
    (?P<episode_number>[^<]+)
    (?:<[^>]+>)+                      # Multiple tags
    (?P<name>[^<]+)
    (?:<[^>]+>)+                      # Multiple tags
    (?P<rerun>(?:\s+\(Wdh.\))?)
"""


def scrape_wunschliste(html: Optional[str] = None) \
        -> Iterable[Episode]:
    """Scrape episodes from wunschliste.de"""

    def get_html() -> str:
        response = requests.get(WUNSCHLISTE_URL,
                                params=WUNSCHLISTE_QUERY_PARAMETERS,
                                timeout=30)
        response.raise_for_status()
        return response.text

    def parse_episodes(html_source: str) \
            -> Iterable[tuple[str, Optional[Match[str]]]]:
        return (
            (
                episode_html,
                re.search(WUNSCHLISTE_PARSE_EPISODE_PATTERN,
                          episode_html)
            )
            for episode_html
            in re.findall(WUNSCHLISTE_SELECT_EPISODE_PATTERN,
                          html_source)
        )

    def cleanup_html(html_dict: dict[str, str]) -> dict[str, str]:
        return {
            key: re.sub(r'(?m)(?:\s|\\n)+(?=\s|\\n)', '', value)
            for key, value in html_dict.items()
        }

    def to_episode(raw_episode_dict: dict[str, str]) -> Episode:
        return Episode(
            int(raw_episode_dict['episode_number']),
            name=raw_episode_dict['name'],
            date_published=datetime(
                int(raw_episode_dict['year']),
                int(raw_episode_dict['month']),
                int(raw_episode_dict['day']),
                hour=int(raw_episode_dict['hour']),
                minute=int(raw_episode_dict['minute']),
                tzinfo=WUNSCHLISTE_IMPLIED_TIMEZONE,
            ),
            sd_date_published=datetime.now(),
            is_rerun=bool(raw_episode_dict['rerun']),
            is_spinoff=not raw_episode_dict['name'].startswith('Folge'),
            timezone=WUNSCHLISTE_IMPLIED_TIMEZONE,
        )

    for episode_html, episode_match \
            in parse_episodes(html or get_html()):
        if not episode_match:
            raise RuntimeError(
                f'Unable to parse episode from {repr(episode_html)}')
        if episode_match.groupdict()['day']:
            yield to_episode(
                cleanup_html(episode_match.groupdict())
            )
