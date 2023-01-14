import re
from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
from typing import List


@dataclass
class Program:
    date: str = ""
    title: str = ""
    members: List[str] = field(default_factory=list)


def scrape_programs(debug=False) -> List[Program]:
    """
    2週分のプログラムを取ってくる。デバッグ時はローカルのファイルを読むようにする。
    """
    programs = [Program(), Program()]
    if debug:
        html = open('/home/hiratako/work/junk_app_develop/next_ametalk_scraper/next_ametalk_scraper/2023_01_10_lineup.html', 'r').read()
    else:
        session = HTMLSession()
        try:
            r = session.get("https://www.tv-asahi.co.jp/ametalk/lineup/")
        except requests.exceptions.ConnectionError:
            print("テレ朝が忙しいっぽい")
            exit(1)
        html = r.html.html
    soup = BeautifulSoup(html, "html.parser")
    found = soup.find_all("div", class_="cn-box page-box lt-radius-la")
    for i, item in enumerate(found):
        # date, title を抽出する
        pre_proccessed_str = item.find("h3")\
                                 .text.replace("\n", "")\
                                      .replace(" ", "")
        date, title = re.split(r"(?<=）)", pre_proccessed_str)
        programs[i].date = date
        programs[i].title = title
        # members を抽出する
        members_p_list = item.find("div", class_="txt-box summernote").find_all("p")[2:-1]
        for p_item in members_p_list:
            programs[i].members += p_item.text.replace("\n", "").split("＆")
        programs[i].members = [member for member in programs[i].members if member]  # 空文字を削除
    return programs


if __name__ == '__main__':
    programs = scrape_programs()
    for program in programs:
        print(f"放送日：{program.date}")
        print(f"タイトル：{program.title}")
        print(f"出演者：{' '.join(program.members)}\n")
