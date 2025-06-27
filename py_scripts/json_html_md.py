"get html for all json articles, then convert it to markdown"

from pathlib import Path
import requests
import glob
from bs4 import BeautifulSoup
import json
import time
from sodatools import read_path, write_path, str_path

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
}


def fetch_url_and_convert_to_md(url, msgid, html_dir: Path):
    if not html_dir.joinpath(f"{msgid}.html").exists():
        r = requests.get(url=url, headers=headers)
        retry = 1
        while r.status_code != 200 and retry < 5:
            retry += 1
            r = requests.get(url=url, headers=headers)
        if r.status_code != 200:
            print(r"fetch {url} error")
            exit(-1)

        time.sleep(10)  # reduce server pressure
        html_dir.joinpath(f"{msgid}.html").write_bytes(r.content)

    html = read_path(html_dir.joinpath(f"{msgid}.html"))
    soup = BeautifulSoup(html, "html.parser")

    contents = soup.find_all("div", "rich_media_content")[0].contents
    content = "\n\n".join(map(lambda x: x.text, contents))

    p = f"""+++
date = '$date'
title = '$title'
+++

{content}"""
    return p


def json_html_md(json_dir: Path, html_dir: Path, markdown_dir: Path):
    files = list(sorted(glob.glob("*.json", root_dir=str_path(json_dir)), reverse=True))

    for file in files:
        obj1 = json.loads(read_path(json_dir.joinpath(file)))
        for article in obj1["getalbum_resp"]["article_list"]:
            title = article["title"]
            md_name = title.replace(" | ", "-")

            url = article["url"]
            msgid = article["msgid"]
            date = article["create_time"]
            import datetime

            date = datetime.datetime.fromtimestamp(int(date))
            date = date.isoformat() + "+08:00"

            body = fetch_url_and_convert_to_md(url, msgid, html_dir=html_dir)
            body = body.replace("$date", date)
            body = body.replace("$title", title)

            write_path(markdown_dir.joinpath(f"{md_name}.md"), body)

            print(md_name)
