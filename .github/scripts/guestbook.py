"""Add one guestbook signature to README.md, from the issue in TITLE / LOGIN / NUMBER.

The issue title is a stranger's text: it goes into a code span with backticks, control and
invisible characters removed, so nothing in it renders as markdown, HTML, a link or a mention.
"""
import datetime
import os
import re
import sys
from pathlib import Path

START, END = "<!-- guestbook:start -->", "<!-- guestbook:end -->"
KEEP = 10  # newest signatures shown
MAX_CHARS = 140


def clean(title: str) -> str:
    msg = title.split(":", 1)[1] if ":" in title else title
    msg = "".join(c if c.isprintable() and c != "`" else " " for c in msg)
    msg = " ".join(msg.split())[:MAX_CHARS].strip()
    return msg or "was here"


def sign(readme: str, login: str, number: str, title: str, today: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9-]+(\[bot\])?", login) or not number.isdigit():
        raise ValueError(f"unexpected login or issue number: {login!r} {number!r}")
    head, rest = readme.split(START, 1)
    body, tail = rest.split(END, 1)
    mark = f"<!-- #{number} -->"
    if mark in body:
        return readme  # this issue already signed
    old = [line for line in body.splitlines() if line.startswith("- **")]
    line = f"- **[{login}](https://github.com/{login})** · {today} · `{clean(title)}` {mark}"
    return head + START + "\n" + "\n".join([line, *old][:KEEP]) + "\n" + END + tail


if __name__ == "__main__":
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "README.md")
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    text = path.read_text(encoding="utf-8")
    path.write_text(
        sign(text, os.environ["LOGIN"], os.environ["NUMBER"], os.environ["TITLE"], today),
        encoding="utf-8",
        newline="\n",
    )
