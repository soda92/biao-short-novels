from pathlib import Path
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
}


url = "http://mp.weixin.qq.com/s?__biz=Mzg4NTc2OTYxMQ==&mid=2247484365&idx=1&sn=2e8a3e1016e7ea5b46613ff888372472&chksm=cfa29729f8d51e3ffce20c1aa4cc6de1d7e125d4a09fc3e8534916083b6fa831a8252ceacd38#rd"

r = requests.get(url=url, headers=headers)

print(r.status_code)

Path("s_2.html").write_bytes(r.content)
