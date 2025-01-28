from pathlib import Path
import re
import shutil
import requests


def get():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    }

    args0 = {
        "action": "getalbum",
        "album_id": "3329839945947119618",
    }

    r = requests.get(
        url="https://mp.weixin.qq.com/mp/appmsgalbum", headers=headers, params=args0
    )

    Path("start.html").write_bytes(r.content)


get()

content = Path("start.html").read_text(encoding="utf8")

pattern = '<span class="js_article_create_time album__item-info-item">([0-9]*)</span>'
t = re.findall(pattern, content)[0]

pattern = "https://mmbiz.qpic.cn/mmbiz_jpg/[0-9a-zA-Z]+/300"
img = re.findall(pattern, content)[0]

pattern = 'data-link="(.*)"'
url = re.findall(pattern, content)[0]
url = url.replace("&amp;", "&")

pattern = 'data-msgid="([0-9]+)"'
msgid = re.findall(pattern, content)[0]

pattern = 'data-title="(.*)"'
title = re.findall(pattern, content)[0]

structure = (
    """
{
  "base_resp": {
    "exportkey_token": "",
    "ret": 0
  },
  "getalbum_resp": {
    "article_list": [
      {
        "cover_img_1_1": "{img}",
        "cover_theme_color": {
          "b": "30",
          "g": "35",
          "r": "31"
        },
        "create_time": "{t}",
        "is_pay_subscribe": "0",
        "is_read": "0",
        "item_show_type": "0",
        "itemidx": "1",
        "key": "3885769611_2247484415_1",
        "msgid": "{msgid}",
        "pos_num": "76",
        "title": "{title}",
        "tts_is_ban": "0",
        "url": "{url}",
        "user_read_status": "0"
      }
    ]
  }
}""".replace("{t}", t)
    .replace("{img}", img)
    .replace("{url}", url)
    .replace("{msgid}", msgid)
    .replace("{title}", title)
)

print(structure)

shutil.rmtree("json")
Path("json").mkdir(parents=True, exist_ok=True)
Path("json").joinpath(msgid + ".json").write_text(structure, encoding="utf8")
