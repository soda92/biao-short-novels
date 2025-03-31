"find articles that has no number in the title, and assign number corresponding to json order"

import glob
import json
from pathlib import Path
from sodatools import read_path, write_path, str_path


def fix_names(json_dir: Path, markdown_dir: Path, dest_dir: Path):
    # clean_file_dir(Path("generated_markdown/a.md"))

    SEQ = 0
    files = list(sorted(glob.glob("*.json", root_dir=str_path(json_dir)), reverse=True))

    for file in files:
        file_p = json_dir.joinpath(file)
        obj1 = json.loads(read_path(file_p))
        for article in obj1["getalbum_resp"]["article_list"]:
            title = article["title"]
            new_title = title
            if "|" in title:
                SEQ = int(title.split("|")[0].strip())
            else:
                SEQ -= 1
                new_title = f"{SEQ} | {title}"

            old_md_name = title.replace(" | ", "-")
            old_md_file = markdown_dir.joinpath(f"{old_md_name}.md")

            new_md_name = new_title.replace(" | ", "-")
            new_md_file = dest_dir.joinpath(f"{new_md_name}.md")

            content = read_path(old_md_file)
            content = content.replace(title, new_title)
            write_path(new_md_file, content)
