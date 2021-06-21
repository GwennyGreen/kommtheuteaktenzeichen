"""Transforms an EpisodePresentResponse into a context dict."""

from datetime import datetime
from typing import Literal

import flask
from markupsafe import Markup

from kha.formatters.episode_check_response_formatter \
    import EpisodeCheckResponseFormatter
from kha.episode_check_response import EpisodePresentResponse
from kha.local_types \
    import AnswerPropertyName, DatetimeInUserTimezone, \
    IsoDatetimeStr, PageContextDict, RichContentMarkupStr
from kha.settings \
    import TV_SERIES_LONG_NAME, TV_NETWORK, USER_TIMEZONE
from kha.verdict import Verdict


class EpisodePresentResponseFormatter(EpisodeCheckResponseFormatter):
    """Transforms an EpisodePresentResponse into a context dict."""

    def __init__(self, response: EpisodePresentResponse):
        super().__init__()
        self.response = response

    @property
    def iso_sd_date_published(self) -> IsoDatetimeStr:
        return self.response.sd_date_published

    @property
    def positive(self) -> bool:
        return self._verdict() == Verdict.YES

    def answer_property_name(self) -> AnswerPropertyName:
        return 'acceptedAnswer'

    def long_explanation_restricted_markup(self) \
            -> RichContentMarkupStr:
        return RichContentMarkupStr(
            f'{self._episode_name()} von {TV_SERIES_LONG_NAME}'
            + f' kommt am {self._formatted_start_date()}'
            + f' im {TV_NETWORK}.'
        )

    def short_explanation(self) -> Markup:
        return Markup(flask.render_template(
            'short_explanation.template.html',
            formatted_start_date=self._formatted_start_date(),
            iso_start_date=self._iso_start_date(),
            Markup=Markup,
            tv_network=TV_NETWORK,
            Verdict=Verdict,
            verdict=self._verdict(),
        ))

    def to_context(self) -> PageContextDict:
        return {
            'title': self.title,
            'faq_page_seo_json': self._faq_page_seo_json(),
            'question': self.question,
            'verdict': self._verdict(),
            'verdict_statement': self.verdict_statement(),
            'formatted_start_date': self._formatted_start_date(),
            'short_explanation': self.short_explanation(),
            'answer_known': True,
            'iso_sd_date_published': self.iso_sd_date_published,
            'formatted_sd_date_published':
            self._formatted_sd_date_published(),
            'reaction': self._random_reaction(),
        }

    def verdict_statement(self) -> str:
        return {
            Verdict.YES: 'Ja',
            Verdict.NO: 'Nein',
        }[self._verdict()]

    def _episode_name(self) -> str:
        return self.response.episode_name

    def _formatted_start_date(self) -> str:
        # pylint: disable=no-member
        return self._start_date() \
            .strftime(f'%A, {self._start_date().day}.'
                      + '\N{NO-BREAK SPACE}%B'
                      + '\N{NO-BREAK SPACE}%Y'
                      + ' um %H:%M\N{NO-BREAK SPACE}Uhr')

    def _iso_start_date(self) -> IsoDatetimeStr:
        return self.response.start_date

    def _start_date(self) -> DatetimeInUserTimezone:
        return DatetimeInUserTimezone(
            datetime.fromisoformat(self._iso_start_date())
                    .astimezone(USER_TIMEZONE)
        )

    def _sd_date_published(self) -> DatetimeInUserTimezone:
        """
        Timestamp of the moment the response has been compiled.
        """
        return DatetimeInUserTimezone(
            datetime.fromisoformat(self.iso_sd_date_published)
                    .astimezone(USER_TIMEZONE)
        )

    def _verdict(self) -> Literal[Verdict.YES, Verdict.NO]:
        return self.response.verdict
