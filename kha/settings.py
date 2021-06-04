"""Shared paths and settings"""

from pathlib import Path

import dateutil.tz

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
PACKAGE_ROOT = Path(__file__).parent.absolute()

SITE_NAME = 'Kommt heute Aktenzeichen?'
TV_SERIES_LONG_NAME = 'Aktenzeichen XY … ungelöst'
TV_NETWORK = 'ZDF'

EVENTS_JSON_FILENAME = 'events.kha.json'
LOCAL_EVENTS_JSON_PATH = \
    PROJECT_ROOT / 'etc' / EVENTS_JSON_FILENAME
S3_BUCKET_NAME = 'kha-store'

USER_TIMEZONE = dateutil.tz.gettz('Europe/Berlin')
USER_LOCALE = 'de_DE'

WUNSCHLISTE_URL = 'https://www.wunschliste.de/ajax/epg_liste.pl'
WUNSCHLISTE_QUERY_PARAMETERS = {
    's': '1187',
    'station': '2',
}
WUNSCHLISTE_IMPLIED_TIMEZONE = dateutil.tz.gettz('Europe/Berlin')


POSITIVE_REACTIONS = [
    '💯',
    '🥰',
    '🎉',
    '🔝',
    'Großartig 😍',
    'Ehrenwebsite 👌',
    'Danke',
    'thx',
    '😬',
    '🤩',
    '🦹🔫👮',
    '🆗🆒',
]

NEGATIVE_REACTIONS = [
    '😢',
    '🥺 menno',
    'Ach müü.',
    '🤷',
    'aber warum',
    'k',
    'thx',
    'Na ok',
    '😾',
    '😒',
    '😕',
    '😩',
    '😭',
    '😠',
    '😐',
    '🙄',
    '😞',
    'Danke Merkel',
]
