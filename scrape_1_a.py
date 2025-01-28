from pathlib import Path
import re

content = Path("s_m.html").read_text(encoding="utf8")

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
        }
    }
}""".replace("{t}", t)
    .replace("{img}", img)
    .replace("{url}", url)
    .replace("{msgid}", msgid)
    .replace("{title}", title)
)

print(structure)
