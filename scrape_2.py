from pathlib import Path
import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
}


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

    msgid = get_last_msgid(r2)

    Path(f"json/{msgid}.json").write_bytes(r.content)


if __name__ == "__main__":
    import glob

    f = list(sorted(glob.glob("json/*.json"), reverse=True))

    f = f[0]
    r = json.loads(Path(f).read_text(encoding="utf8"))

    msgid = get_last_msgid(r)
    print(msgid)
    get(msgid)
