from pathlib import Path
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
}

args = {
    "action": "getalbum",
    "__biz": "",
    "album_id": "3329839945947119618",
    "count": "10",
    "begin_msgid": "2247484420",
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

print(r.status_code)

Path("s0.json").write_bytes(r.content)
