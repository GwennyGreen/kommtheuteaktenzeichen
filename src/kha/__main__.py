"""Entry point for the CLI."""

import fire

import api
import fire_workarounds

fire_workarounds.apply()
fire.Fire({
    'check': api.check_episode
})
