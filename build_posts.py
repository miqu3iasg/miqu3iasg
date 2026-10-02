import json
import pathlib
import re
from datetime import datetime

ROOT = pathlib.Path(__file__).parent.resolve()
POSTS_FILE = ROOT / "linkedin-posts.json"
README = ROOT / "README.md"
MARKER = "linkedin"
LIMIT = 5


def load_posts():
    posts = json.loads(POSTS_FILE.read_text(encoding="utf-8"))
    for post in posts:
        datetime.strptime(post["date"], "%Y-%m-%d")  # validate date format
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts[:LIMIT]


def render(posts):
    if not posts:
        return "No posts listed yet."
    return "\n\n".join(f"[{p['title']}]({p['url']}) - {p['date']}" for p in posts)


def replace_chunk(content, marker, chunk):
    pattern = re.compile(rf"<!-- {marker} start -->.*?<!-- {marker} end -->", re.DOTALL)
    return pattern.sub(
        lambda _: f"<!-- {marker} start -->\n{chunk}\n<!-- {marker} end -->", content
    )


if __name__ == "__main__":
    chunk = render(load_posts())
    README.write_text(
        replace_chunk(README.read_text(encoding="utf-8"), MARKER, chunk),
        encoding="utf-8",
    )
    print(chunk)
