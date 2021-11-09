"""Shared paths and settings"""

from pathlib import Path

import dateutil.tz

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
PACKAGE_ROOT = Path(__file__).parent.absolute()

SITE_NAME = 'Kommt heute Aktenzeichen?'
TV_SERIES_LONG_NAME = 'Aktenzeichen XY … ungelöst'
TV_NETWORK = 'ZDF'

EVENTS_JSON_BUCKET_DEV = 'kha-store-dev'
EVENTS_JSON_BUCKET_PROD = 'kha-store'
EVENTS_JSON_FILENAME = 'events.kha.json'
LOCAL_EVENTS_JSON_PATH = \
    PROJECT_ROOT / 'etc' / EVENTS_JSON_FILENAME

USER_TIMEZONE = dateutil.tz.gettz('Europe/Berlin')
USER_LOCALE = 'de_DE'

WUNSCHLISTE_URL = 'https://www.wunschliste.de/ajax/epg_liste.pl'
WUNSCHLISTE_QUERY_PARAMETERS = {
    's': '1187',
    'station': '2',
}
WUNSCHLISTE_IMPLIED_TIMEZONE = dateutil.tz.gettz('Europe/Berlin')


FAVICONS_MANIFEST = {
    'name': SITE_NAME,
    'short_name': SITE_NAME,
    'icons': [
        {
            'src': '/android-chrome-192x192.png',
            'sizes': '192x192',
            'type': 'image/png',
        },
        {
            'src': '/android-chrome-512x512.png',
            'sizes': '512x512',
            'type': 'image/png',
        }
    ],
    'theme_color': '#ffffff',
    'background_color': '#ffffff',
    'display': 'standalone',
}


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
]
