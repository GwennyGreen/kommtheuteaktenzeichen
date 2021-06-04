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
    return {
        'name': settings.SITE_NAME,
        'short_name': settings.SITE_NAME,
        'icons': [
            {
                'src': '/android-chrome-192x192.png',
                'sizes': '192x192',
                'type': 'image/png',
            },
            {
                'src': '/android-chrome-512x512.png',
                'sizes': '512x512',
                'type': 'image/png',
            }
        ],
        'theme_color': '#ffffff',
        'background_color': '#ffffff',
        'display': 'standalone',
    }


def test_s3():
    """Test S3 connectivity."""
    print('Printing episode list')
    print(kha.api.all_episodes_from_s3())
    print('Done printing episode list')
