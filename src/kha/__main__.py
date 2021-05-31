"""Entry point for the CLI."""

import fire

import fire_workarounds
import kha.api as api

fire_workarounds.apply()
fire.Fire({
    'check': api.check_episode
})
