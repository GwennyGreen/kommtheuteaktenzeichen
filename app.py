"""The main app."""

from datetime import datetime
import locale
import random

import dateutil.tz
from flask import Flask, url_for

import kha.api
from kha.verdict import Verdict

SITE_NAME = 'Kommt heute Aktenzeichen?'
TV_SERIES_LONG_NAME = 'Aktenzeichen XY … ungelöst'
TV_NETWORK = 'ZDF'
USER_TIMEZONE = dateutil.tz.gettz('Europe/Berlin')
USER_LOCALE = 'de_DE'

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


locale.setlocale(locale.LC_ALL, USER_LOCALE)
app = Flask('kha')


@app.route('/')
def main():
    """Main page."""
    def formatted_start_date(response):
        start_date = datetime \
            .fromisoformat(response['start_date']) \
            .astimezone(USER_TIMEZONE)
        return start_date \
            .strftime(f'%A, {start_date.day}.\N{NO-BREAK SPACE}%B\N{NO-BREAK SPACE}%Y'
                      + ' um %H:%M\N{NO-BREAK SPACE}Uhr')

    def formatted_sd_date_published(response):
        sd_date_published = datetime \
            .fromisoformat(response['sd_date_published']) \
            .astimezone(USER_TIMEZONE)
        return sd_date_published \
            .strftime(f'{sd_date_published.day}.'
                      + '\N{NO-BREAK SPACE}%B'
                      + '\N{NO-BREAK SPACE}%Y')

    def short_explanation(response):
        return {
            Verdict.YES: f'Heute, {formatted_start_date(response)} im {TV_NETWORK}.',
            Verdict.NO: f'Erst am {formatted_start_date(response)}.',
            Verdict.UNKNOWN: 'In unserer Datenbank steht das gerade nicht drin.',
        }[response['verdict']]

    def long_explanation(response):
        return short_explanation(response) \
        if response['verdict'] == Verdict.UNKNOWN \
        else f'{response["episode_name"]} von {TV_SERIES_LONG_NAME}' \
        + f' kommt am {formatted_start_date(response)} im {TV_NETWORK}.'

    def positive(response):
        return response['verdict'] == Verdict.YES

    response = kha.api.check()
    page_context = {
        'title': SITE_NAME,
        'verdict': response['verdict'],
        'verdict_statement': {
            Verdict.YES: 'Ja',
            Verdict.NO: 'Nein',
            Verdict.UNKNOWN: 'Keine Ahnung',
        }[response['verdict']],
        'formatted_start_date': formatted_start_date(response),
        'short_explanation': short_explanation(response),
        'long_explanation': long_explanation(response),
        'answer_known': response['verdict'] != Verdict.UNKNOWN,
        'sd_date_published': response['sd_date_published'],
        'formatted_sd_date_published':
        formatted_sd_date_published(response),
        'reaction':
        random.choice(POSITIVE_REACTIONS
                      if positive(response)
                      else NEGATIVE_REACTIONS),
    }
    return f"""
    <html lang="de">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
        <link rel="apple-touch-icon" sizes="180x180" href="{url_for('static', filename='favicon/apple-touch-icon.png')}">
        <link rel="icon" type="image/png" sizes="32x32" href="{url_for('static', filename='favicon/favicon-32x32.png')}">
        <link rel="icon" type="image/png" sizes="16x16" href="{url_for('static', filename='favicon/favicon-16x16.png')}">
        <link rel="manifest" href="{url_for('webmanifest')}">
        <link rel="stylesheet" href="{url_for('static', filename='default.css')}">
        <title>{page_context['title']}</title>
        <script type="application/ld+json">
            {{
                "@context": "http://schema.org/",
                "@type": "FAQPage",
                "mainEntity": [
                    {{
                        "@context": "http://schema.org/",
                        "@type": "Question",
                        "name": "Kommt heute Aktenzeichen?",
                        "answerCount": 1,
                        "{'acceptedAnswer' if page_context['answer_known'] else 'suggestedAnswer'}": {{
                            "@context": "http://schema.org/",
                            "@type": "Answer",
                            "text": "<strong>{page_context['verdict_statement']}.</strong><br>{page_context['short_explanation']}"
                        }},
                        "answerExplanation": {{
                            "text": "{page_context['long_explanation']}"
                        }}
                    }}
                ],
                "mainContentOfPage": {{
                    "xpath": "/html/body/main"
                }},
                "speakable": {{
                    "xpath": "/html/body/main"
                }},
                "sdDatePublished": "{page_context['sd_date_published']}"
            }}
        </script>
    </head>
    <body>
    <main>
        <p class="bubble them">Kommt heute Aktenzeichen?</p>
        <h1 class="bubble us">{page_context['verdict_statement']}.</h1>
        <p class="smol dangling us">Stand: {page_context['formatted_sd_date_published']}</p>
        <p class="bubble us">{page_context['short_explanation']}</p>
        <p class="bubble them">{page_context['reaction']}</p>
    </main>
    <nav>
        <ul>
            <li><a href="{url_for('static', filename='impressum.html')}">Impressum</a></li>
            <li><a href="{url_for('static', filename='datenschutz.html')}">Datenschutz</a></li>
        </ul>
    </nav>
    </body>
    </html>
    """


@app.route('/site.webmanifest')
def webmanifest():
    """A web app manifest for favicons and other things."""
    return f"""
    {
        "name": "{SITE_NAME}",
        "short_name": "{SITE_NAME}",
        "icons": [
            {
                "src": "/android-chrome-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/android-chrome-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ],
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "display": "standalone"
    }
    """


def test_s3():
    """Test S3 connectivity."""
    print('Printing episode list')
    print(kha.api.all_episodes_from_s3())
    print('Done printing episode list')
