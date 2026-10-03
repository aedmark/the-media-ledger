"""One lookup of each kind against the real Open Library, to catch it changing its replies.

Skipped unless LIVE=1. It makes two requests; a 429 (rate limit) skips rather than fails, because it says nothing
about the code.
"""
import os

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.skipif(os.environ.get("LIVE") != "1", reason="live test: set LIVE=1 to run")


def test_live_isbn_search(page, app_url):
    page.goto(app_url)
    page.wait_for_function("() => typeof db !== 'undefined' && db !== undefined")
    page.fill("#isbn", "9780439708180")
    page.click("#search-form button[type=submit]")
    staged = page.locator("#staging-area:not(.hidden)")
    toast = page.locator("#toast-container")
    expect(staged.or_(toast.locator("div"))).to_be_visible(timeout=20000)
    if "limiting searches" in toast.inner_text():
        pytest.skip("Open Library answered 429 (rate limited)")
    expect(page.locator("#staged-book-details")).to_contain_text("Harry Potter")
    expect(page.locator("#staged-book-details")).to_contain_text("9780439708180")


def test_live_title_search(page, app_url):
    page.goto(app_url)
    page.wait_for_function("() => typeof db !== 'undefined' && db !== undefined")
    page.check("input[value=title]")
    page.fill("#title", "Dune")
    page.fill("#author", "Frank Herbert")
    page.click("#search-form button[type=submit]")
    staged = page.locator("#staging-area:not(.hidden)")
    toast = page.locator("#toast-container")
    expect(staged.or_(toast.locator("div"))).to_be_visible(timeout=20000)
    if "limiting searches" in toast.inner_text():
        pytest.skip("Open Library answered 429 (rate limited)")
    expect(page.locator("#staged-book-details")).to_contain_text("Dune")
    expect(page.locator("#staged-book-details")).to_contain_text("Frank Herbert")
