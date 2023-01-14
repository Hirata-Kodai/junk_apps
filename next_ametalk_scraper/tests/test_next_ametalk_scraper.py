from next_ametalk_scraper import __version__
from next_ametalk_scraper.Scraper import scrape_programs, Program
from typing import List


def test_version():
    assert __version__ == '0.1.0'


def test_scrape_programs():
    programs: List[Program] = scrape_programs(debug=True)
    assert programs[0].date == "1月12日（木）"
    assert programs[0].title == "プロ麻雀・Mリーグ芸人"
    assert programs[0].members == ["爆笑問題・田中", "平成ノブシコブシ徳井", "シソンヌじろう", \
                                   "ロバート山本", "インスタントジョンソンじゃい", "ティモンディ前田", \
                                   "モグライダーともしげ", "陣内智則"]
    assert programs[1].date == "1月19日（木）"
    assert programs[1].title == "やっぱり！コロッケ芸人"
    assert programs[1].members == ["博多華丸", "ケンドーコバヤシ", "サンドウィッチマン伊達", \
                                   "ブラックマヨネーズ小杉", "ロバート秋山", "ぼる塾・田辺", \
                                   "東京０３飯塚 "]
