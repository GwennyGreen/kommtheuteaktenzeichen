"""Entry point for the command line interface."""

import sys

import fire  # type: ignore

from . import api, fire_workarounds


def run(*args: str) -> None:
    """Runs the command line interface."""
    fire_workarounds.apply()
    fire.Fire({
        'check': api.check_episode,
        'list': api.list_eligible_episodes,
        'print': {
            'dev': api.print_episodes_dev,
            'prod': api.print_episodes_prod,
        }
    }, command=list(args) + sys.argv[1:]
    )
