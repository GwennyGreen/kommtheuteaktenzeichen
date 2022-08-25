"""Entry point for the command line interface."""

import fire

from kha import api, fire_workarounds


def run() -> None:
    """Runs the command line interface."""
    fire_workarounds.apply()
    fire.Fire({
        'check': api.check_episode,
        'list': api.list_eligible_episodes,
        'print': {
            'dev': api.print_episodes_dev,
            'prod': api.print_episodes_prod,
        },
    })
