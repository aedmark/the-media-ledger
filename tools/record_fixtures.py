#!/usr/bin/env python3
"""Record real Open Library replies for the test fixtures.

    python3 tools/record_fixtures.py          # from the repo root

Makes one request per recorded fixture (four in all), keeps only the fields the app reads, and overwrites the files
in tests/fixtures/open_library/. Review the diff before committing. Standard library only; no API key.
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tests" / "fixtures" / "open_library"
BASE = "https://openlibrary.org"
SEARCH_FIELDS = "title,author_name,first_publish_year,isbn,number_of_pages_median"
# File name -> the request exactly as index.html builds it.
REQUESTS = {
    "isbn_9780439708180.json": "/api/books?bibkeys=ISBN:9780439708180&format=json&jscmd=data",
    "isbn_not_found.json": "/api/books?bibkeys=ISBN:9798888888884&format=json&jscmd=data",
    "search_dune_frank_herbert.json": f"/search.json?title=Dune&fields={SEARCH_FIELDS}&limit=1&author=Frank%20Herbert",
    "search_empty.json": f"/search.json?title=zzqxjv%20nonexistent&fields={SEARCH_FIELDS}&limit=1",
}
# Open Library asks API users to identify themselves.
HEADERS = {"User-Agent": "LibraryLedger-fixture-recorder (https://github.com/aedmark/the-media-ledger)"}


def trim(reply):
    if "docs" in reply:  # search.json
        return {"numFound": reply.get("numFound", 0),
                "docs": [{k: (v[:10] if k == "isbn" else v)  # a work can list hundreds of ISBNs
                          for k, v in doc.items() if k in SEARCH_FIELDS.split(",")} for doc in reply["docs"]]}
    trimmed = {}  # api/books: {"ISBN:...": edition}
    for key, edition in reply.items():
        ids = edition.get("identifiers", {})
        trimmed[key] = {
            "title": edition.get("title"),
            "authors": [{"name": a.get("name")} for a in edition.get("authors", [])],
            "publish_date": edition.get("publish_date"),
            "number_of_pages": edition.get("number_of_pages"),
            "identifiers": {k: v for k, v in ids.items() if k in ("isbn_13", "isbn_10")},
        }
        trimmed[key] = {k: v for k, v in trimmed[key].items() if v not in (None, [], {})}
    return trimmed


def main():
    for name, path in REQUESTS.items():
        request = urllib.request.Request(BASE + path, headers=HEADERS)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                reply = json.load(response)
        except urllib.error.HTTPError as error:
            print(f"{name}: HTTP {error.code}; nothing written.")
            return 1
        (OUT / name).write_text(json.dumps(trim(reply), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{name}: recorded")
    print("Now check the Source column in tests/fixtures/open_library/README.md and rerun the tests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
