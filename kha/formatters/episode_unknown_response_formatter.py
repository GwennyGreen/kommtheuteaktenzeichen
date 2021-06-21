"""Transforms an EpisodeUnknownResponse into a context dict."""

from markupsafe import Markup

from kha.formatters.episode_check_response_formatter \
    import EpisodeCheckResponseFormatter
from kha.episode_check_response import EpisodeUnknownResponse
from kha.local_types \
    import AnswerPropertyName, IsoDatetimeStr, PageContextDict, \
    RichContentMarkupStr
from kha.verdict import Verdict


class EpisodeUnknownResponseFormatter(EpisodeCheckResponseFormatter):
    """Transforms an EpisodeUnknownResponse into a context dict."""

    def __init__(self, response: EpisodeUnknownResponse):
        super().__init__()
        self.response = response

    @property
    def iso_sd_date_published(self) -> IsoDatetimeStr:
        return self.response.sd_date_published

    @property
    def positive(self) -> bool:
        return False

    def answer_property_name(self) -> AnswerPropertyName:
        return 'suggestedAnswer'

    def long_explanation_restricted_markup(self) \
            -> RichContentMarkupStr:
        return self._short_explanation_restricted_markup()

    def short_explanation(self) -> Markup:
        return Markup(
            'In unserer Datenbank steht das gerade nicht drin.'
        )

    def to_context(self) -> PageContextDict:
        return {
            'title': self.title,
            'faq_page_seo_json': self._faq_page_seo_json(),
            'question': self.question,
            'verdict': Verdict.UNKNOWN,
            'verdict_statement': self.verdict_statement(),
            'formatted_start_date': None,
            'short_explanation': self.short_explanation(),
            'answer_known': False,
            'iso_sd_date_published': self.iso_sd_date_published,
            'formatted_sd_date_published':
            self._formatted_sd_date_published(),
            'reaction': self._random_reaction(),
        }

    def verdict_statement(self) -> str:
        return 'Keine Ahnung'
