"""Package-scoped type annotations."""

from datetime import datetime
from typing import Literal, NewType, TypedDict

from .episode import Episode
from .verdict import Verdict


AnswerPropertyName = Literal['acceptedAnswer', 'suggestedAnswer']
DatetimeInUserTimezone = NewType('DatetimeInUserTimezone', datetime)
FaqPageSeoJson = NewType('FaqPageSeoJson', str)
HumanReadableDatetime = NewType('HumanReadableDatetime', str)
IsoDatetimeStr = NewType('IsoDatetimeStr', str)
Reaction = NewType('Reaction', str)
RichContentMarkupStr = NewType('RichContentMarkupStr', str)
Uuid = NewType('Uuid', str)


class EventsDict(TypedDict):
    """Top-level dictionary."""
    episodes: dict[Uuid, Episode]


class PageContextDict(TypedDict):
    """Dictionary to feed the HTML template."""
    title: str
    faq_page_seo_json: str
    question: str
    verdict: Verdict
    verdict_statement: str
    formatted_start_date: str | None
    short_explanation: str
    answer_known: bool
    iso_sd_date_published: str
    formatted_sd_date_published: str
    reaction: str
