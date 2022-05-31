"""
Factory methods for transforming an EpisodeCheckResponse into a
context dict for rendering the HTML template.
"""

from functools import singledispatch
from typing import Union
from kha.formatters.episode_check_response_formatter \
    import EpisodeCheckResponseFormatter
from kha.formatters.episode_present_response_formatter \
    import EpisodePresentResponseFormatter
from kha.formatters.episode_unknown_response_formatter \
    import EpisodeUnknownResponseFormatter

from .episode_check_response \
    import EpisodePresentResponse, EpisodeUnknownResponse


@singledispatch
def formatter_for(__response: Union[
    EpisodePresentResponse,
    EpisodeUnknownResponse
]) -> EpisodeCheckResponseFormatter:
    """
    Returns a formatter that can transform an EpisodeCheckResponse
    into a context dict for rendering the HTML template.
    """
    ...


@formatter_for.register
def _(response: EpisodePresentResponse) \
        -> EpisodeCheckResponseFormatter:
    return EpisodePresentResponseFormatter(response)


@formatter_for.register
def _(response: EpisodeUnknownResponse) \
        -> EpisodeCheckResponseFormatter:
    return EpisodeUnknownResponseFormatter(response)
