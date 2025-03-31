"from the first json, get all json"

from pathlib import Path
import requests
import json
from sodatools import write_path, read_path, str_path
import glob
import functools
from typing import List

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


def download_json_from(msgid):
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


def write(json_obj, destdir: Path):
    msgid = get_last_msgid(json_obj)
    print(msgid)

    write_path(
        destdir.joinpath(f"{msgid}.json"),
        json.dumps(json_obj, indent=2, ensure_ascii=False),
    )


@functools.cache
def get_all_msgids(json_dir: Path) -> List[str]:
    ret = []
    fs = list(sorted(glob.glob("*.json", root_dir=str_path(json_dir)), reverse=True))
    for file in fs:
        file_p = json_dir.joinpath(file)
        obj = json.loads(read_path(file_p))
        article_list = obj["getalbum_resp"]["article_list"]
        for article in article_list:
            ret.append(article["msgid"])

    return ret


def msgid_already_downloaded(msgid: str, json_dir: Path) -> bool:
    all_msgids = get_all_msgids(json_dir=json_dir)
    return msgid in all_msgids


def get_latest_json_file_content(json_dir: Path):
    f = list(sorted(glob.glob("*.json", root_dir=str_path(json_dir)), reverse=True))

    f = json_dir.joinpath(f[0])
    r = json.loads(read_path(f))
    return r


def get_all_json(json_dir: Path):
    while True:
        r = get_latest_json_file_content(json_dir=json_dir)
        msgid = get_last_msgid(r)
        print(msgid)

        obj = download_json_from(msgid)

        if "article_list" not in obj["getalbum_resp"]:
            break
        else:
            write(obj, json_dir)
            break

    print("finished")
