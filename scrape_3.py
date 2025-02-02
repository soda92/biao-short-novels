from pathlib import Path
import requests  # noqa: F401
import glob
from bs4 import BeautifulSoup
import json
import time
from scrape_1 import read_path, write_path, clean_file_dir  # noqa: F401

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
}


def parse(url, msgid):
    r = requests.get(url=url, headers=headers)
    assert r.status_code == 200
    Path(f"generated_html/{msgid}.html").write_bytes(r.content)

    # code adapted from: https://github.com/Ziheng-Liang/wechat_web_scraper/blob/e8030244323c7f9cb4cf6d87b1244861ab691057/selenium/singlePage.py#L8-L20
    html = read_path(Path(f"generated_html/{msgid}.html"))
    soup = BeautifulSoup(html, "html.parser")

    contents = soup.find_all("div", "rich_media_content")[0].contents
    content = "\n\n".join(map(lambda x: x.text, contents))

    p = f"""+++
date = '$date'
title = '$title'
+++

{content}"""
    return p


if __name__ == "__main__":
    # clean_file_dir(Path("generated_markdown/a.md"))

    G_count = 0
    files = list(sorted(glob.glob("generated_json/*.json"), reverse=True))

    for file in files:
        obj1 = json.loads(read_path(Path(file)))
        for article in obj1["getalbum_resp"]["article_list"]:
            title = article["title"]
            url = article["url"]
            msgid = article["msgid"]
            date = article["create_time"]
            import datetime

            date = datetime.datetime.fromtimestamp(int(date))
            date = date.isoformat() + "+08:00"

            body = parse(url, msgid)
            body = body.replace("$date", date)
            body = body.replace("$title", title)

            md_name = title.replace(" | ", "-")
            write_path(Path(f"generated_markdown/{md_name}.md"), body)

            G_count += 1
            # for testing
            # if G_count >= 1:
            #     exit()

            time.sleep(10)
            print(md_name)
