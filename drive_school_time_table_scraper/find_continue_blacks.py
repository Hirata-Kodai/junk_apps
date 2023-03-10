"""
千歳自動車学校のHPから第一段階の学科を連続して受けられる時間帯を探し、出力するスクリプト
"""
from dataclasses import dataclass
from datetime import datetime

import click
from bs4 import BeautifulSoup
from requests_html import HTMLSession

OPEN_TIMES = [f"{i+9}:00" for i in range(11)]


@dataclass
class CourseData:
    date_day: str
    time: str
    number: str


def td_has_crimson_style(td, look_louka):
    return td.get("style") == "color: crimson;"


def td_has_not_crimson_style(td, look_kouka):
    if look_kouka:
        return td.get("style") != "color: crimson;" and td.text != " "
    else:
        return td.get("style") != "color: crimson;" and td.text not in [" ", "効"]


def scrape_latest_timetable():
    """
    最新の時間割をスクレイピングしてくる関数
    """
    this_month = datetime.now().month
    session = HTMLSession()
    url = f"http://chitose-ds.co.jp/chds/timetable-20220{this_month}-{this_month+1}/"
    r = session.get(url)
    if r.status_code == 200:
        return r.html
    else:
        url = f"http://chitose-ds.co.jp/chds/timetable-20220{this_month}/"
        r = session.get(url)
        if r.status_code == 200:
            return r.html
        else:
            raise RuntimeError("fail to scrape")


def get_time_table_matrix():
    """
    時間割をスクレイピングし、行列形式で返す
    """
    html = scrape_latest_timetable()  # requests_html.HTML
    mat = []
    soup = BeautifulSoup(html.html, 'html.parser')
    # tableの取得
    table = soup.find('table')
    # tbodyの解析
    tbody = table.find('tbody')
    trs = tbody.find_all("tr")
    for tr in trs:
        r = []  # 各行を保存
        th_tds = tr.find_all(["th", "td"])
        for th_td in th_tds:
            r.append(th_td)
        mat.append(r)  # 行をテーブルに保存
    return mat


@click.command()
@click.option("--look-kouka", is_flag=True, help="効果検定も見る")
@click.option("--include-not-continuous", is_flag=True, default=False)
def main(look_kouka, include_not_continuous):
    mat = get_time_table_matrix()
    mat_T = list(map(list, zip(*mat)))  # 列ごとに見やすいように転置
    for col in mat_T[1:]:
        if not include_not_continuous:
            prev_courseData = None
            for i, now_td in enumerate(col):
                if i % 2 != 1:  # とりあえず各時間帯の1行目のみを見ることにする
                    continue
                if td_has_crimson_style(now_td, look_kouka):
                    if prev_courseData:  # 連続判定
                        print(prev_courseData.date_day,
                              f"{prev_courseData.time}~{OPEN_TIMES[(i-1) // 2]}",
                              prev_courseData.number, now_td.text)  # 日付、時間、番号 の順で出力
                        prev_courseData = CourseData(col[0].text, OPEN_TIMES[(i-1) // 2], now_td.text)
                    else:
                        prev_courseData = CourseData(col[0].text, OPEN_TIMES[(i-1) // 2], now_td.text)
                        continue
                else:
                    prev_courseData = None
        else:
            for i, now_td in enumerate(col):
                if i % 2 != 1:  # とりあえず各時間帯の1行目のみを見ることにする
                    continue
                if td_has_crimson_style(now_td, look_kouka):
                    print(col[0].text,
                          OPEN_TIMES[(i-1) // 2],
                          now_td.text)  # 日付、時間、番号 の順で出力


if __name__ == '__main__':
    main()
