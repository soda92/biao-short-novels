from .get_first import scrape_1, Path
from .get_all_json import scrape_2
from .json_html_md import scrape_3
from .z0_fix_names import fix_names

if __name__ == "__main__":
    scrape_1()
    scrape_2()
    scrape_3()

    C = Path(__file__).resolve().parent
    R = C.parent
    json_dir = R.joinpath("generated_json")
    markdown_dir = R.joinpath("generated_markdown")
    dest_dir = R.joinpath("content").joinpath("post")
    fix_names(json_dir=json_dir, markdown_dir=markdown_dir, dest_dir=dest_dir)
