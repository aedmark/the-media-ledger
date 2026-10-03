"""Shared fixtures: serve the repo locally and keep every test off the real network.

Each test gets a fresh browser context (pytest-playwright), so IndexedDB starts empty.
Open Library is answered from tests/fixtures/open_library/; Tailwind is replaced by the one rule the app's logic
depends on (`.hidden`); any other outside request is aborted and fails the test.
"""
import functools
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures" / "open_library"
OPEN_LIBRARY = "https://openlibrary.org/"
# Lookup key (see BookSource.key) -> fixture file. Unlisted ISBNs and titles get the recorded "not found" replies.
DEFAULT_REPLIES = {
    "isbn:9780439708180": "isbn_9780439708180.json",
    "title:Dune author:Frank Herbert": "search_dune_frank_herbert.json",
}
NOT_FOUND = {"isbn": "isbn_not_found.json", "title": "search_empty.json"}
# Tailwind's `hidden` utility is what shows and hides the staging area, list, and spinner.
TAILWIND_STUB = "document.head.insertAdjacentHTML('beforeend', '<style>.hidden{display:none!important}</style>');"


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="session")
def app_url():
    handler = functools.partial(_QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}/"
    server.shutdown()


class BookSource:
    """Answers Open Library requests from fixtures and records what the app asked for."""

    def __init__(self):
        self.replies = dict(DEFAULT_REPLIES)
        self.lookups = []  # decoded keys, in order: "isbn:<isbn>" or "title:<title>[ author:<author>]"
        self.raw_urls = []
        self.next_status = None  # e.g. 429: the next request gets this status instead of a fixture
        self.fail_network = False

    def reply_with(self, lookup, fixture):
        self.replies[lookup] = fixture

    @staticmethod
    def key(url):
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if parsed.path == "/api/books":
            return "isbn:" + params.get("bibkeys", [""])[0].removeprefix("ISBN:")
        key = "title:" + params.get("title", [""])[0]
        if "author" in params:
            key += " author:" + params["author"][0]
        return key

    def handle(self, route):
        url = route.request.url
        self.raw_urls.append(url)
        lookup = self.key(url)
        self.lookups.append(lookup)
        if self.fail_network:
            return route.abort("internetdisconnected")
        if self.next_status:
            status, self.next_status = self.next_status, None
            return route.fulfill(status=status, content_type="text/html", body="<html>error</html>",
                                 headers={"Access-Control-Allow-Origin": "*"})
        name = self.replies.get(lookup, NOT_FOUND[lookup.split(":")[0]])
        body = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
        route.fulfill(status=200, json=body, headers={"Access-Control-Allow-Origin": "*"})


@pytest.fixture
def library():
    return BookSource()


@pytest.fixture
def app(page, app_url, library):
    """The app, loaded with its database open, and with every outside request intercepted."""
    stray = []

    def outside(route):
        url = route.request.url
        if url.startswith(OPEN_LIBRARY):
            return library.handle(route)
        if url.startswith("https://cdn.tailwindcss.com"):
            return route.fulfill(status=200, content_type="application/javascript", body=TAILWIND_STUB)
        if not url.startswith("https://fonts."):
            stray.append(url)
        route.abort()

    page.route(lambda url: not url.startswith(app_url), outside)
    page.on("dialog", lambda dialog: pytest.fail(f"unexpected dialog: {dialog.message}"))
    page.goto(app_url)
    page.wait_for_function("() => typeof db !== 'undefined' && db !== undefined")
    yield page
    assert not stray, f"the app tried to reach the network: {stray}"
