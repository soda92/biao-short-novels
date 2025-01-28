import glob
import json
from pathlib import Path
from scrape_1 import read_path, write_path

if __name__ == "__main__":
    # clean_file_dir(Path("generated_markdown/a.md"))

    SEQ = 0
    files = list(sorted(glob.glob("generated_json/*.json"), reverse=True))

    for file in files:
        obj1 = json.loads(read_path(Path(file)))
        for article in obj1["getalbum_resp"]["article_list"]:
            title = article["title"]
            new_title = title
            if "|" in title:
                SEQ = int(title.split("|")[0].strip())
            else:
                SEQ -= 1
                new_title = f"{SEQ} | {title}"

            old_md_name = title.replace(" | ", "-")
            old_md_file = Path(f"generated_markdown/{old_md_name}.md")

            new_md_name = new_title.replace(" | ", "-")
            new_md_file = Path(f"content/post/{new_md_name}.md")

            content = read_path(old_md_file)
            content = content.replace(title, new_title)
            write_path(new_md_file, content)
