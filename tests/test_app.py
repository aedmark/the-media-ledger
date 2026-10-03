"""End-to-end checks of a user's path through the app, with Google Books answered from fixtures (conftest.py).

Each test corresponds to a step of the manual smoke test or a roadmap item in docs/TESTING.md.
"""
import csv
import io

import pytest
from playwright.sync_api import expect


def search_isbn(page, isbn):
    page.check("input[value=isbn]")
    page.fill("#isbn", isbn)
    page.click("#search-form button[type=submit]")


def search_title(page, title, author=""):
    page.check("input[value=title]")
    page.fill("#title", title)
    page.fill("#author", author)
    page.click("#search-form button[type=submit]")


def commit(page, duplicate=False):
    # The save finishes asynchronously; reloading or searching before it does races the IndexedDB write.
    page.click("#btn-save-book")
    if duplicate:
        expect(page.locator("#toast-container")).to_contain_text("already in your ledger")
    else:
        expect(page.locator("#staging-area")).to_be_hidden()


def saved_records(page):
    return page.evaluate("""() => new Promise(resolve => {
        const request = db.transaction(['books']).objectStore('books').getAll();
        request.onsuccess = () => resolve(request.result);
    })""")


def reload(page):
    page.reload()
    page.wait_for_function("() => typeof db !== 'undefined' && db !== undefined")


def export_csv(page):
    with page.expect_download() as download:
        page.click("#btn-export")
    with open(download.value.path(), encoding="utf-8") as f:
        return list(csv.reader(io.StringIO(f.read())))


def test_starts_empty(app):
    expect(app.locator("#empty-state")).to_be_visible()
    expect(app.locator("#ledger-list")).to_be_hidden()


def test_isbn_search_stages_the_first_result(app, google):
    search_isbn(app, "978-0-439-70818-0")
    expect(app.locator("#staging-area")).to_be_visible()
    expect(app.locator("#staged-book-details")).to_contain_text("Harry Potter and the Sorcerer's Stone")
    expect(app.locator("#staged-book-details")).to_contain_text("9780439708180")
    assert google.queries == ["isbn:9780439708180"]  # dashes stripped


def test_commit_saves_and_survives_reload(app):
    search_isbn(app, "9780439708180")
    commit(app)
    expect(app.locator("#ledger-list li")).to_have_count(1)
    expect(app.locator("#staging-area")).to_be_hidden()
    reload(app)
    expect(app.locator("#ledger-list h4")).to_have_text(["Harry Potter and the Sorcerer's Stone"])
    [record] = saved_records(app)
    assert record["isbn"] == "9780439708180"
    assert record["author"] == "J. K. Rowling"
    assert record["publishedYear"] == "1999"
    assert record["pages"] == 312


def test_duplicate_isbn_is_not_saved_twice(app):
    search_isbn(app, "9780439708180")
    commit(app)
    search_isbn(app, "9780439708180")
    expect(app.locator("#staging-area")).to_be_visible()
    commit(app, duplicate=True)
    assert len(saved_records(app)) == 1


def test_title_and_author_search(app, google):
    search_title(app, "Dune", "Frank Herbert")
    expect(app.locator("#staged-book-details")).to_contain_text("Dune")
    commit(app)
    expect(app.locator("#ledger-list li")).to_have_count(1)
    assert google.queries == ["intitle:Dune inauthor:Frank Herbert"]


def test_book_without_isbn_is_saved_as_na(app, google):
    google.reply_with("intitle:Pamphlet", "no_isbn.json")
    search_title(app, "Pamphlet")
    commit(app)
    [record] = saved_records(app)
    assert record["isbn"] == "N/A"
    assert record["author"] == "Unknown Author"


def test_no_results_says_so(app):
    search_isbn(app, "0000000000")
    expect(app.locator("#toast-container")).to_contain_text("No books found")
    expect(app.locator("#staging-area")).to_be_hidden()
    expect(app.locator("#search-spinner")).to_be_hidden()


def test_rate_limit_is_reported_as_such(app, google):  # P1-05
    google.next_status = 429
    search_isbn(app, "9780439708180")
    expect(app.locator("#toast-container")).to_contain_text("limiting searches")
    expect(app.locator("#toast-container")).not_to_contain_text("No books found")
    expect(app.locator("#search-spinner")).to_be_hidden()


def test_other_http_errors_name_the_status(app, google):  # P1-05
    google.next_status = 503
    search_isbn(app, "9780439708180")
    expect(app.locator("#toast-container")).to_contain_text("HTTP 503")


def test_network_failure_is_reported(app, google):
    google.fail_network = True
    search_isbn(app, "9780439708180")
    expect(app.locator("#toast-container")).to_contain_text("Network error")
    expect(app.locator("#search-spinner")).to_be_hidden()


def test_isbn_is_url_encoded(app, google):  # P1-05
    search_isbn(app, "978&q=x#y")
    expect(app.locator("#toast-container")).to_contain_text("No books found")
    assert google.raw_urls[-1].endswith("q=isbn:978%26q%3Dx%23y")
    assert google.queries == ["isbn:978&q=x#y"]


def test_remove_survives_reload(app):
    search_isbn(app, "9780439708180")
    commit(app)
    search_title(app, "Dune", "Frank Herbert")
    commit(app)
    expect(app.locator("#ledger-list li")).to_have_count(2)
    app.locator("#ledger-list li", has_text="Harry Potter").get_by_title("Remove").click()
    expect(app.locator("#ledger-list li")).to_have_count(1)
    reload(app)
    expect(app.locator("#ledger-list h4")).to_have_text(["Dune"])


def test_export_csv(app):
    search_isbn(app, "9780439708180")
    commit(app)
    search_title(app, "Dune", "Frank Herbert")
    commit(app)
    expect(app.locator("#ledger-list li")).to_have_count(2)
    rows = export_csv(app)
    assert rows == [
        ["Title", "Author", "ISBN", "Published Year", "Pages"],
        ["Harry Potter and the Sorcerer's Stone", "J. K. Rowling", "9780439708180", "1999", "312"],
        ["Dune", "Frank Herbert", "9780441013593", "2005", "528"],
    ]


def test_export_with_empty_ledger_says_so(app):
    app.click("#btn-export")
    expect(app.locator("#toast-container")).to_contain_text("Nothing to export")


def test_hostile_book_renders_as_text(app, google):  # P1-02
    google.reply_with("intitle:Hostile", "hostile.json")
    search_title(app, "Hostile")
    expect(app.locator("#staged-book-details")).to_contain_text("<img src=x onerror=")
    commit(app)
    reload(app)
    expect(app.locator("#ledger-list h4")).to_contain_text("<img src=x onerror=")
    expect(app.locator("#ledger-list")).to_contain_text("<b>Bold</b> & 'Quoted'")
    assert app.locator("#ledger-list img, #ledger-list svg[onload], #staged-book-details img").count() == 0
    assert app.evaluate("() => window.__pwned") is None
    app.get_by_title("Remove").click()
    assert saved_records(app) == []


@pytest.mark.xfail(strict=True, reason="P1-03: CSV cells are not yet guarded against formulas")
def test_export_neutralises_spreadsheet_formulas(app, google):
    google.reply_with("intitle:Hostile", "hostile.json")
    search_title(app, "Hostile")
    commit(app)
    expect(app.locator("#ledger-list li")).to_have_count(1)
    author = export_csv(app)[1][1]
    assert not author.startswith(("=", "+", "-", "@"))
