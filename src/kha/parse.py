"""Parse episodes from online sources."""

from datetime import datetime
import re

import dateutil.tz
import requests

from episode import Episode

WUNSCHLISTE_URL = 'https://www.wunschliste.de/ajax/epg_liste.pl'
WUNSCHLISTE_QUERY_PARAMETERS = {
    's': '1187',
    'station': '2',
}

WUNSCHLISTE_IMPLIED_TIMEZONE = dateutil.tz.gettz('Europe/Berlin')
WUNSCHLISTE_SELECT_EPISODE_PATTERN = r'(?ms)<li.*?</li>'

WUNSCHLISTE_PARSE_EPISODE_PATTERN = r"""(?msx)
    [A-Z][a-z],[^<]+                  # Weekday
    (?P<day>\d{2})\.
    (?P<month>\d{2})\.
    <.*?>                             # Multiple text nodes or tags
    (?P<year>\d{4})
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


def parse_wunschliste():
    """Parse episodes from wunschliste.de"""

    def parse_episodes(html_source):
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

    def cleanup_html(html_dict):
        return {
            key: re.sub(r'(?m)(?:\s|\\n)+(?=\s|\\n)', '', value)
            for key, value in html_dict.items()
        }

    def to_episode(raw_episode_dict):
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
            tz=WUNSCHLISTE_IMPLIED_TIMEZONE,
        )

    response = requests.get(WUNSCHLISTE_URL,
                            params=WUNSCHLISTE_QUERY_PARAMETERS)
    response.raise_for_status()
    for episode_html, episode_match in parse_episodes(response.text):
        if not episode_match:
            raise RuntimeError(
                f'Unable to parse episode from {repr(episode_html)}')
        yield to_episode(cleanup_html(episode_match.groupdict()))
