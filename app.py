"""The main app."""

import locale

import flask

import kha.api
from kha.format import EpisodeCheckResponseFormatter
import kha.settings as settings


locale.setlocale(locale.LC_ALL, settings.USER_LOCALE)
app = flask.Flask('kha')


@app.route('/')
def main():
    """Main page."""
    formatter = EpisodeCheckResponseFormatter(kha.api.check())
    return flask.render_template('main.template.html',
                                 **formatter.to_context())


@app.route('/site.webmanifest')
def webmanifest():
    """A web app manifest for favicons and other things."""
    return settings.FAVICONS_MANIFEST


def test_s3():
    """Test S3 connectivity."""
    print('Printing episode list')
    print(kha.api.all_episodes_from_store())
    print('Done printing episode list')
