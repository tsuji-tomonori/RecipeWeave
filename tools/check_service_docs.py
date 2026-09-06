"""Check generated manual links, including Japanese section anchors, without a browser."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if identifier := values.get("id"):
            self.ids.add(identifier)
        for attribute in ("href", "src"):
            if reference := values.get(attribute):
                self.refs.append(reference)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?", default="frontend/public/help")
    args = parser.parse_args()
    directory = Path(args.directory).resolve()
    pages: dict[Path, References] = {}
    for path in directory.rglob("*.html"):
        parsed = References()
        parsed.feed(path.read_text())
        pages[path] = parsed
    if not pages:
        raise SystemExit("no generated manual pages")
    errors: list[str] = []
    for path, parsed in pages.items():
        for reference in parsed.refs:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.is_file():
                errors.append(f"{path.name}: missing {reference}")
            elif url.fragment and target in pages:
                if unquote(url.fragment) not in pages[target].ids:
                    errors.append(f"{path.name}: missing anchor {reference}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Manual links, images and anchors passed: {len(pages)} HTML pages")


if __name__ == "__main__":
    main()
