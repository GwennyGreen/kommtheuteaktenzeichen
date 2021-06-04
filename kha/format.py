# pylint: disable=too-few-public-methods

"""Transforms an EpisodeCheckResponse into a context dict."""

from datetime import datetime
import json
import random
from typing import TypedDict

import flask
from markupsafe import Markup

from .episode_check_response import EpisodeCheckResponse
from .settings import NEGATIVE_REACTIONS, POSITIVE_REACTIONS, \
    SITE_NAME, TV_SERIES_LONG_NAME, TV_NETWORK, USER_TIMEZONE
from .verdict import Verdict


class PageContextDict(TypedDict):
    """Dictionary to feed the HTML template."""
    title: str
    faq_page_seo_json: str
    question: str
    verdict: Verdict
    verdict_statement: str
    formatted_start_date: str
    short_explanation: str
    answer_known: bool
    iso_sd_date_published: str
    formatted_sd_date_published: str
    reaction: str


class EpisodeCheckResponseFormatter:
    """Transforms an EpisodeCheckResponse into a context dict."""

    def __init__(self, response: EpisodeCheckResponse):
        self.question: str = 'Kommt heute Aktenzeichen?'
        self.response: EpisodeCheckResponse = response

    def to_context(self) -> PageContextDict:
        """Returns a dict to feed the HTML template."""
        return {
            'title': SITE_NAME,
            'faq_page_seo_json': self._faq_page_seo_json(),
            'question': self.question,
            'verdict': self._verdict(),
            'verdict_statement': self._verdict_statement(),
            'formatted_start_date': self._formatted_start_date(),
            'short_explanation': self._short_explanation(),
            'answer_known': self._answer_known(),
            'iso_sd_date_published': self._iso_sd_date_published(),
            'formatted_sd_date_published':
            self._formatted_sd_date_published(),
            'reaction': self._random_reaction(),
        }

    def _verdict(self):
        return self.response['verdict']

    def _verdict_statement(self):
        """A brief phrase that expresses the verdict."""
        return {
            Verdict.YES: 'Ja',
            Verdict.NO: 'Nein',
            Verdict.UNKNOWN: 'Keine Ahnung',
        }[self._verdict()]

    def _start_date(self):
        return datetime \
            .fromisoformat(self._iso_start_date()) \
            .astimezone(USER_TIMEZONE)

    def _iso_start_date(self):
        return self.response['start_date']

    def _formatted_start_date(self):
        return self._start_date() \
            .strftime(f'%A, {self._start_date().day}.'
                      + '\N{NO-BREAK SPACE}%B'
                      + '\N{NO-BREAK SPACE}%Y'
                      + ' um %H:%M\N{NO-BREAK SPACE}Uhr')

    def _sd_date_published(self):
        """
        Returns the point in time at which the response has been
        compiled.
        """
        return datetime \
            .fromisoformat(self._iso_sd_date_published()) \
            .astimezone(USER_TIMEZONE)

    def _iso_sd_date_published(self):
        return self.response['sd_date_published']

    def _formatted_sd_date_published(self):
        return self._sd_date_published() \
            .strftime(f'{self._sd_date_published().day}.'
                      + '\N{NO-BREAK SPACE}%B'
                      + '\N{NO-BREAK SPACE}%Y')

    def _short_explanation(self):
        """A sentence that explains the verdict."""
        return Markup(flask.render_template(
            'short_explanation.template.html',
            formatted_start_date=self._formatted_start_date(),
            iso_start_date=self._iso_start_date(),
            Markup=Markup,
            tv_network=TV_NETWORK,
            Verdict=Verdict,
            verdict=self._verdict(),
        ))

    def _short_explanation_restricted_markup(self):
        """
        A sentence that explains the verdict.
        Honors the restricted set of markup that Google allows for
        rich content.
        """
        return Markup(self._short_explanation()).striptags()

    def _long_explanation_restricted_markup(self):
        """
        A sentence that explains the verdict in a bit more detail.
        Honors the restricted set of markup that Google allows for
        rich content.
        """
        return self._short_explanation_restricted_markup() \
            if self._verdict() == Verdict.UNKNOWN \
            else f'{self._episode_name()} von {TV_SERIES_LONG_NAME}' \
            + f' kommt am {self._formatted_start_date()}' \
            + f' im {TV_NETWORK}.'

    def _answer_html_restricted_markup(self):
        return flask.render_template(
            'seo_structured_answer.template.html',
            verdict_statement=self._verdict_statement(),
            short_explanation=self
            ._short_explanation_restricted_markup(),
        )

    def _answer_known(self):
        """Returns False for `Verdict.UNKNOWN`, True otherwise."""
        return self._verdict() != Verdict.UNKNOWN

    def _positive(self):
        return self._verdict() == Verdict.YES

    def _episode_name(self):
        return self.response['episode_name']

    def _answer_property_name(self):
        return 'acceptedAnswer' if self._answer_known() \
            else 'suggestedAnswer'

    def _random_reaction(self):
        return random.choice(POSITIVE_REACTIONS
                             if self._positive()
                             else NEGATIVE_REACTIONS)

    def _faq_page_seo_json(self) -> str:
        """
        Transforms an EpisodeCheckResponse into a FAQPage structure
        for rich data SEO and renders it as JSON.
        """
        return json.dumps({
            '@context': 'http://schema.org/',
            '@type': 'FAQPage',
            'name': Markup.escape(self.question),
            'mainEntity': [
                {
                    '@context': 'http://schema.org/',
                    '@type': 'Question',
                    'name': Markup.escape(self.question),
                    'answerCount': 1,
                    self._answer_property_name(): {
                        '@context': 'http://schema.org/',
                        '@type': 'Answer',
                        'text': Markup.escape(
                            self._answer_html_restricted_markup()
                        ),
                    },
                    'answerExplanation': {
                        '@context': 'http://schema.org/',
                        '@type': 'Comment',
                        'text': Markup.escape(
                            self
                            ._long_explanation_restricted_markup()
                        ),
                    }
                }
            ],
            'mainContentOfPage': {
                '@context': 'http://schema.org/',
                '@type': 'WebPageElement',
                'xpath': '/html/body/main',
            },
            'speakable': {
                '@context': 'http://schema.org/',
                '@type': 'WebPageElement',
                'xpath': '/html/body/main',
            },
            'sdDatePublished':
            self._sd_date_published().isoformat(timespec='seconds')
        })
