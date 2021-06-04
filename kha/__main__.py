"""Entry point for the CLI."""

import fire

import kha.api as api
import kha.fire_workarounds as fire_workarounds

fire_workarounds.apply()
fire.Fire({
    'check': api.check_episode
})
