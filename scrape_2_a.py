import json
from pathlib import Path
import glob
from scrape_2 import get, get_last_msgid

f = list(sorted(glob.glob("json/*.json")))
latest = Path(f[0]).read_text(encoding="utf8")

r = json.loads(latest)

msgid = get_last_msgid(r)

get(msgid)
