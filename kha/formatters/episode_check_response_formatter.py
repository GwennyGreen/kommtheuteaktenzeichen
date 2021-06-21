# pylint: disable=too-few-public-methods

"""Transforms an EpisodeCheckResponse into a context dict."""

from abc import ABC, abstractmethod
from datetime import datetime
import json
import random

from dateutil.relativedelta import relativedelta
import flask
from markupsafe import Markup

from kha.local_types \
    import AnswerPropertyName, DatetimeInUserTimezone, \
    FaqPageSeoJson, HumanReadableDatetime, IsoDatetimeStr, PageContextDict, \
    Reaction, RichContentMarkupStr
from kha.settings \
    import NEGATIVE_REACTIONS, POSITIVE_REACTIONS, SITE_NAME, \
    USER_TIMEZONE


class EpisodeCheckResponseFormatter(ABC):
    """Transforms an EpisodeCheckResponse into a context dict."""

    def __init__(self) -> None:
        self.title: str = SITE_NAME
        self.question: str = 'Kommt heute Aktenzeichen?'

    @property
    @abstractmethod
    def iso_sd_date_published(self) -> IsoDatetimeStr:
        """
        Timestamp of the moment the response has been compiled,
        formatted as an ISO datetime string.
        """
        ...

    @property
    @abstractmethod
    def positive(self) -> bool:
        """Whether or not the verdict yields a positive reaction."""
        ...

    @abstractmethod
    def answer_property_name(self) -> AnswerPropertyName:
        """
        The name of the answer property to use in the FAQ page SEO
        structure.
        """
        ...

    @abstractmethod
    def long_explanation_restricted_markup(self) \
            -> RichContentMarkupStr:
        """
        A sentence that explains the verdict in a bit more detail.
        Honors the restricted set of markup that Google allows for
        rich content.
        """
        ...

    @abstractmethod
    def short_explanation(self) -> Markup:
        """A sentence that explains the verdict."""
        ...

    @abstractmethod
    def to_context(self) -> PageContextDict:
        """Returns a dict to feed the HTML template."""
        ...

    @abstractmethod
    def verdict_statement(self) -> str:
        """A brief phrase that expresses the verdict."""
        ...

    def _answer_html_restricted_markup(self) \
            -> RichContentMarkupStr:
        return RichContentMarkupStr(
            flask.render_template(
                'seo_structured_answer.template.html',
                verdict_statement=self.verdict_statement(),
                short_explanation=self
                ._short_explanation_restricted_markup(),
            )
        )

    def _date_modified(self) -> DatetimeInUserTimezone:
        """
        Timestamp of the start of the current day, according to
        the assumed user’s time zone.
        """
        return DatetimeInUserTimezone(
            self._sd_date_published() + relativedelta(
                hour=0, minute=0, second=0, microsecond=0)
        )

    def _random_reaction(self) -> Reaction:
        return Reaction(random.choice(POSITIVE_REACTIONS
                                      if self.positive
                                      else NEGATIVE_REACTIONS))

    def _formatted_sd_date_published(self) -> HumanReadableDatetime:
        return HumanReadableDatetime(
            # pylint: disable=no-member
            self._sd_date_published()
            .strftime(f'{self._sd_date_published().day}.'
                      + '\N{NO-BREAK SPACE}%B'
                      + '\N{NO-BREAK SPACE}%Y')
        )

    def _sd_date_published(self) -> DatetimeInUserTimezone:
        """
        Timestamp of the moment the response has been compiled.
        """
        return DatetimeInUserTimezone(
            datetime.fromisoformat(self.iso_sd_date_published)
                    .astimezone(USER_TIMEZONE)
        )

    def _faq_page_seo_json(self) -> FaqPageSeoJson:
        """
        Transforms an EpisodePresentResponse into a FAQPage structure
        for rich data SEO and renders it as JSON.
        """
        return FaqPageSeoJson(json.dumps({
            '@context': 'http://schema.org/',
            '@type': 'FAQPage',
            'name': Markup.escape(self.question),
            'headline': Markup.escape(self.question),
            'dateModified':
                self._date_modified()  # pylint: disable=no-member
                .isoformat(timespec='seconds'),
            'datePublished': '2021-06-03T23:50:00+02:00',
            'sdDatePublished':
                self._sd_date_published()  # pylint: disable=no-member
                .isoformat(timespec='seconds'),
            'mainEntity': [
                {
                    '@context': 'http://schema.org/',
                    '@type': 'Question',
                    'name': Markup.escape(self.question),
                    'answerCount': 1,
                    self.answer_property_name(): {
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
                            .long_explanation_restricted_markup()
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
        }))

    def _short_explanation_restricted_markup(self) \
            -> RichContentMarkupStr:
        """
        A sentence that explains the verdict.
        Honors the restricted set of markup that Google allows for
        rich content.
        """
        return RichContentMarkupStr(
            self.short_explanation().striptags()
        )
