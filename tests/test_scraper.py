# pylint: disable=missing-function-docstring, missing-module-docstring, no-self-use

from kha.episode import Episode
import pytest

import kha.scraper

@pytest.fixture(name='episode_569_html')
def fixture_episode_569_html() -> str:
    return """<li id="2_0" class="tvneu lp" onClick="epg_details('GD5_ORf2wnkBB_yvw7w1yqI6','2_0');"><label class="la"><span class="w180-80" title="ZDF"><strong class="no-smartphone">ZDF</strong><strong class="smartphone">ZDF</strong></span><span class="w100-70">heute</span><span class="w50">20:15 h</span></label><span class="ft340-210"><label class="se"><label class="epg_ep" title="Episode">568</label></label><strong>Folge 568</strong><span class="hinweis">NEU</span></span></li><div id="t_2_0" class="epg_text"><!-- #epg_GD5_ORf2wnkBB_yvw7w1yqI6|2_0 --></div><li id="2_1" class="lp" onClick="epg_details('GD5_lYD2wnkBgUpm-GP7ytRx','2_1');"><label class="la"><span class="w180-80" title="ZDF"><strong class="no-smartphone">ZDF</strong><strong class="smartphone">ZDF</strong></span><span class="w100-70">morgen</span><span class="w50">03:15 h</span></label><span class="ft340-210"><label class="se"><label class="epg_ep" title="Episode">568</label></label><strong>Folge 568</strong> (Wdh.)</span></li><div id="t_2_1" class="epg_text"></div><li id="2_2" class="tvneu lp" onClick="epg_details('GD5_h4w1d3oBOhLv7hK_pUiw','2_2');"><label class="la"><span class="w180-80" title="ZDF"><strong class="no-smartphone">ZDF</strong><strong class="smartphone">ZDF</strong></span><span class="w100-70">Mi, 18.08.<label class="no-smartphone">2021</label></span><span class="w50">20:15 h</span></label><span class="ft340-210"><label class="se"><label class="epg_ep" title="Episode">569</label></label><strong>Folge 569</strong><span class="hinweis">NEU</span></span></li><div id="t_2_2" class="epg_text"></div><li id="2_3" class="lp" onClick="epg_details('GD5_QkA1d3oBB_yvw7w1pSrv','2_3');"><label class="la"><span class="w180-80" title="ZDF"><strong class="no-smartphone">ZDF</strong><strong class="smartphone">ZDF</strong></span><span class="w100-70">Do, 19.08.<label class="no-smartphone">2021</label></span><span class="w50">03:35 h</span></label><span class="ft340-210"><label class="se"><label class="epg_ep" title="Episode">569</label></label><strong>Folge 569</strong> (Wdh.)</span></li><div id="t_2_3" class="epg_text"></div>"""  # pylint: disable=line-too-long

def test_scrape_episode_569(episode_569_html: str) -> None:
    assert [
        episode.domain_key
        for episode
        in kha.scraper.scrape_wunschliste(episode_569_html)
    ] == [
        (569, False, False),
        (569, True, False),
    ]
