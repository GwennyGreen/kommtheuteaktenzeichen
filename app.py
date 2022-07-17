"""The main app."""

import locale
from typing import Any

import flask

import kha.api
from kha import settings
from kha.format import formatter_for


locale.setlocale(locale.LC_ALL, settings.USER_LOCALE)
app = flask.Flask('kha')


@app.route('/')
def main() -> str:
    """Main page."""
    formatter = formatter_for(kha.api.check())
    return flask.render_template('main.template.html',
                                 **formatter.to_context())


@app.route('/site.webmanifest')
def webmanifest() -> dict[str, Any]:
    """A web app manifest for favicons and other things."""
    return settings.FAVICONS_MANIFEST


def test_s3() -> None:
    """Test S3 connectivity."""
    print('Printing episode list')
    print(kha.api.all_episodes_from_store())
    print('Done printing episode list')
