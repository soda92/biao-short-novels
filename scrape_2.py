from pathlib import Path
import requests
import json
import time
from scrape_1 import write_path, read_path

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
}
"""
empty/error response:
{
  "base_resp": {
    "exportkey_token": "",
    "ret": 0
  },
  "getalbum_resp": {
    "base_info": {
      "is_first_screen": "0"
    },
    "continue_flag": "0",
    "reverse_continue_flag": "1"
  }
}
"""


def get_last_msgid(obj):
    assert "article_list" in obj["getalbum_resp"]
    return obj["getalbum_resp"]["article_list"][-1]["msgid"]


def get(msgid):
    args = {
        "action": "getalbum",
        "__biz": "",
        "album_id": "3329839945947119618",
        "count": "20",
        "begin_msgid": str(msgid),
        "begin_itemidx": "1",
        "uin": "",
        "key": "",
        "pass_ticket": "",
        "wxtoken": "",
        "devicetype": "",
        "clientversion": "",
        "appmsg_token": "",
        "x5": "0",
        "f": "json",
    }

    r = requests.get(
        url="https://mp.weixin.qq.com/mp/appmsgalbum", headers=headers, params=args
    )

    assert r.status_code == 200
    r2 = json.loads(r.content.decode())

    return r2


def write(obj):
    msgid = get_last_msgid(obj)
    print(msgid)

    write_path(
        Path(f"generated_json/{msgid}.json"),
        json.dumps(obj, indent=2, ensure_ascii=False),
    )


if __name__ == "__main__":
    import glob

    f = list(sorted(glob.glob("generated_json/*.json"), reverse=True))
    assert len(f) == 1

    f = Path(f[0])
    r = json.loads(read_path(f))

    msgid = get_last_msgid(r)
    print(msgid)

    obj = get(msgid)

    while "article_list" in obj["getalbum_resp"]:
        write(obj)
        time.sleep(10)

        f = list(sorted(glob.glob("generated_json/*.json")))
        latest = read_path(Path(f[0]))

        r = json.loads(latest)
        msgid = get_last_msgid(r)
        obj = get(msgid)

    print("finished")
