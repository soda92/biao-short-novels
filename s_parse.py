from bs4 import BeautifulSoup
from pathlib import Path
import re

html = Path("s_2.html").read_text(encoding="utf8")
soup = BeautifulSoup(html, "html.parser")
texts = soup.findAll(string=True)


def visible(element):
    if element.parent.name in ["style", "script", "[document]", "head", "title"]:
        return False
    elif re.match("<!--.*-->", element):
        return False
    return True


visible_texts = list(filter(visible, texts))

visible_texts = visible_texts[: visible_texts.index("预览时标签不可点")]
t = "".join(visible_texts)

while "\n\n\n" in t:
    t = t.replace("\n\n\n", "\n\n")
v = list(
    map(
        lambda x: x.strip().replace("\n", "\n\n"),
        filter(lambda x: x != "", t.split("\n\n")),
    )
)

title = v[0].replace(" | ", "-")
content="\n\n".join(title[3:])

p = f"""+++
date = 'date'
title = '{v[0]}'
+++

{content}
"""