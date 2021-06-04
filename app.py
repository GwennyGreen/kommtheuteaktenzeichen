"""The main app."""

from datetime import datetime
import locale
import json

import dateutil.tz
from flask import Flask, url_for

import kha.api
from kha.verdict import Verdict

TV_SERIES_LONG_NAME = 'Aktenzeichen XY … ungelöst'
TV_NETWORK = 'ZDF'
USER_TIMEZONE = dateutil.tz.gettz('Europe/Berlin')
USER_LOCALE = 'de_DE'

locale.setlocale(locale.LC_ALL, USER_LOCALE)
app = Flask('kha')


@app.route('/')
def main():
    """Main page."""
    response = kha.api.check()
    big_verdict = {
        Verdict.YES: 'Ja',
        Verdict.NO: 'Nein',
        Verdict.UNKNOWN: 'Keine Ahnung',
    }[response['verdict']]
    sd_date_published = datetime \
        .fromisoformat(response['sd_date_published']) \
        .astimezone(USER_TIMEZONE)
    start_date = datetime \
        .fromisoformat(response['start_date']) \
        .astimezone(USER_TIMEZONE)
    formatted_sd_date_published = sd_date_published \
        .strftime(f'{sd_date_published.day}.\N{NO-BREAK SPACE}%B\N{NO-BREAK SPACE}%Y')
    formatted_start_date = start_date \
        .strftime(f'%A, {start_date.day}.\N{NO-BREAK SPACE}%B\N{NO-BREAK SPACE}%Y um %H:%M Uhr')
    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
        <link rel="stylesheet" href="{url_for('static', filename='default.css')}">
        <title>Kommt heute Aktenzeichen?</title>
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
                        "{'suggestedAnswer' if response['verdict'] == Verdict.UNKNOWN else 'acceptedAnswer'}": {{
                            "@context": "http://schema.org/",
                            "@type": "Answer",
                            "text": "<strong>{big_verdict}.</strong><br>Erst am {formatted_start_date}."
                        }},
                        "answerExplanation": {{
                            "text": "{response['episode_name']} von {TV_SERIES_LONG_NAME} kommt am {formatted_start_date} im {TV_NETWORK}."
                        }}
                    }}
                ],
                "mainContentOfPage": {{
                    "xpath": "/html/body/main"
                }},
                "speakable": {{
                    "xpath": "/html/body/main"
                }},
                "sdDatePublished": "{response['sd_date_published']}"
            }}
        </script>
    </head>
    <body>
    <main>
        <p class="bubble them">Kommt heute Aktenzeichen?</p>
        <h1 class="bubble us">{big_verdict}.</h1>
        <p class="smol dangling us">Stand: {formatted_sd_date_published}</p>
        <p class="bubble us">Erst am {formatted_start_date}.</p>
        <p class="bubble them">😢</p>
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


def test_s3():
    """Test S3 connectivity."""
    print('Printing episode list')
    print(kha.api.all_episodes_from_s3())
    print('Done printing episode list')
