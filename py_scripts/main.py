from .get_first import get_first, Path
from .get_all_json import get_all_json
from .json_html_md import json_html_md
from .z0_fix_names import fix_names


def main():
    C = Path(__file__).resolve().parent
    R = C.parent
    json_dir = R.joinpath("generated_json")
    html_dir = R.joinpath("generated_html")
    markdown_dir = R.joinpath("generated_markdown")
    dest_dir = R.joinpath("content").joinpath("post")

    get_first(html_dir=html_dir, json_dir=json_dir)
    get_all_json(json_dir=json_dir)
    json_html_md(json_dir=json_dir, markdown_dir=markdown_dir, html_dir=html_dir)

    fix_names(json_dir=json_dir, markdown_dir=markdown_dir, dest_dir=dest_dir)


if __name__ == "__main__":
    main()
