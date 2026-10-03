#!/usr/bin/env python3
"""Record real Google Books replies for the test fixtures.

    python3 tools/record_fixtures.py          # from the repo root, on a network Google is not rate-limiting

Makes one request per recorded fixture (three in all), keeps only the fields the app reads, and overwrites the files
in tests/fixtures/google_books/. Review the diff before committing. Standard library only; no API key.
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tests" / "fixtures" / "google_books"
ENDPOINT = "https://www.googleapis.com/books/v1/volumes?q="
# File name -> the query string exactly as index.html builds it.
QUERIES = {
    "isbn_9780439708180.json": "isbn:9780439708180",
    "title_dune_author_frank_herbert.json": "intitle:Dune+inauthor:Frank%20Herbert",
    "empty.json": "isbn:0000000000",
}
KEEP = ("title", "authors", "publishedDate", "industryIdentifiers", "pageCount")


def trim(reply):
    out = {"kind": reply.get("kind"), "totalItems": reply.get("totalItems", 0)}
    if reply.get("items"):
        out["items"] = [{"kind": item.get("kind"), "id": item.get("id"),
                         "volumeInfo": {k: v for k, v in item.get("volumeInfo", {}).items() if k in KEEP}}
                        for item in reply["items"][:3]]
    return out


def main():
    for name, query in QUERIES.items():
        try:
            with urllib.request.urlopen(ENDPOINT + query, timeout=20) as response:
                reply = json.load(response)
        except urllib.error.HTTPError as error:
            print(f"{name}: HTTP {error.code}; nothing written. A 429 means try later or from another network.")
            return 1
        (OUT / name).write_text(json.dumps(trim(reply), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{name}: recorded ({reply.get('totalItems', 0)} total items)")
    print("Now update the Source column in tests/fixtures/google_books/README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
