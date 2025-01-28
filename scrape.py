import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
}

r = requests.get(
    url="https://mp.weixin.qq.com/mp/appmsgalbum?&action=getalbum&album_id=3329839945947119618",
    headers=headers,
)

print(r.status_code, r.content)
