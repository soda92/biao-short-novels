import requests
from pathlib import Path

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

Path("s_m.html").write_bytes(r.content)
