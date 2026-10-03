"""End-to-end checks of a user's path through the app, with Open Library answered from fixtures (conftest.py).

Each test corresponds to a step of the manual smoke test or a roadmap item in docs/TESTING.md.
"""
import csv

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
    with open(download.value.path(), encoding="utf-8", newline="") as f:  # keep \r inside cells
        return list(csv.reader(f))


def test_page_describes_itself_truthfully(app):  # P1-04
    # The ledger persists in IndexedDB and the page loads outside code, so neither old claim may come back.
    expect(app).to_have_title("Library Ledger | Personal Book Tracker")
    expect(app.locator("body")).not_to_contain_text("in-memory", ignore_case=True)
    expect(app.locator("body")).not_to_contain_text("zero-dependency", ignore_case=True)
    expect(app.get_by_text("Saved in this browser only.")).to_be_visible()


def test_starts_empty(app):
    expect(app.locator("#empty-state")).to_be_visible()
    expect(app.locator("#ledger-list")).to_be_hidden()


def test_isbn_search_stages_the_edition(app, library):
    search_isbn(app, "978-0-439-70818-0")
    expect(app.locator("#staging-area")).to_be_visible()
    expect(app.locator("#staged-book-details")).to_contain_text("Harry Potter and the sorcerer's stone")
    expect(app.locator("#staged-book-details")).to_contain_text("9780439708180")
    assert library.lookups == ["isbn:9780439708180"]  # dashes stripped


def test_commit_saves_and_survives_reload(app):
    search_isbn(app, "9780439708180")
    commit(app)
    expect(app.locator("#ledger-list li")).to_have_count(1)
    expect(app.locator("#staging-area")).to_be_hidden()
    reload(app)
    expect(app.locator("#ledger-list h4")).to_have_text(["Harry Potter and the sorcerer's stone"])
    [record] = saved_records(app)
    assert record["isbn"] == "9780439708180"
    assert record["author"] == "J. K. Rowling"
    assert record["publishedYear"] == "1999"
    assert record["pages"] == 784


def test_duplicate_isbn_is_not_saved_twice(app):
    search_isbn(app, "9780439708180")
    commit(app)
    search_isbn(app, "9780439708180")
    expect(app.locator("#staging-area")).to_be_visible()
    commit(app, duplicate=True)
    assert len(saved_records(app)) == 1


def test_title_and_author_search(app, library):
    search_title(app, "Dune", "Frank Herbert")
    expect(app.locator("#staged-book-details")).to_contain_text("Dune")
    commit(app)
    [record] = saved_records(app)
    assert record["isbn"] == "9780441013593"  # the work's first ISBN-13
    assert record["publishedYear"] == "1965"  # first publication, not this edition
    assert library.lookups == ["title:Dune author:Frank Herbert"]


def test_title_search_prefers_an_isbn_13(app, library):
    library.reply_with("title:Dune", "search_isbn10_first.json")
    search_title(app, "Dune")
    commit(app)
    [record] = saved_records(app)
    assert record["isbn"] == "9780441013593"


def test_book_without_isbn_is_saved_as_na(app, library):
    library.reply_with("title:Pamphlet", "search_no_isbn.json")
    search_title(app, "Pamphlet")
    commit(app)
    [record] = saved_records(app)
    assert record["isbn"] == "N/A"
    assert record["author"] == "Unknown Author"


@pytest.mark.parametrize("search", [lambda p: search_isbn(p, "9798888888884"), lambda p: search_title(p, "zzqxjv")],
                         ids=["isbn", "title"])
def test_no_results_says_so(app, search):
    search(app)
    expect(app.locator("#toast-container")).to_contain_text("No books found")
    expect(app.locator("#staging-area")).to_be_hidden()
    expect(app.locator("#search-spinner")).to_be_hidden()


def test_rate_limit_is_reported_as_such(app, library):  # P1-05
    library.next_status = 429
    search_isbn(app, "9780439708180")
    expect(app.locator("#toast-container")).to_contain_text("limiting searches")
    expect(app.locator("#toast-container")).not_to_contain_text("No books found")
    expect(app.locator("#search-spinner")).to_be_hidden()


def test_other_http_errors_name_the_status(app, library):  # P1-05
    library.next_status = 503
    search_isbn(app, "9780439708180")
    expect(app.locator("#toast-container")).to_contain_text("HTTP 503")


def test_network_failure_is_reported(app, library):
    library.fail_network = True
    search_isbn(app, "9780439708180")
    expect(app.locator("#toast-container")).to_contain_text("Network error")
    expect(app.locator("#search-spinner")).to_be_hidden()


def test_isbn_is_url_encoded(app, library):  # P1-05
    search_isbn(app, "978&q=x#y")
    expect(app.locator("#toast-container")).to_contain_text("No books found")
    assert "bibkeys=ISBN:978%26q%3Dx%23y&" in library.raw_urls[-1]
    assert library.lookups == ["isbn:978&q=x#y"]


def test_title_and_author_are_url_encoded(app, library):
    search_title(app, "War & Peace?", "Tolstoy #1")
    expect(app.locator("#toast-container")).to_contain_text("No books found")
    assert "title=War%20%26%20Peace%3F&" in library.raw_urls[-1]
    assert library.raw_urls[-1].endswith("&author=Tolstoy%20%231")


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
        ["Harry Potter and the sorcerer's stone", "J. K. Rowling", "9780439708180", "1999", "784"],
        ["Dune", "Frank Herbert", "9780441013593", "1965", "608"],
    ]


def test_export_with_empty_ledger_says_so(app):
    app.click("#btn-export")
    expect(app.locator("#toast-container")).to_contain_text("Nothing to export")


def test_hostile_book_renders_as_text(app, library):  # P1-02
    library.reply_with("title:Hostile", "search_hostile.json")
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


def test_export_neutralises_spreadsheet_formulas(app, library):  # P1-03
    library.reply_with("title:Hostile", "search_hostile.json")
    search_title(app, "Hostile")
    commit(app)
    [header, row] = export_csv(app)
    assert len(row) == len(header)  # quotes inside the ISBN did not break the row
    title, author, isbn, year, pages = row
    assert author == "'=HYPERLINK(\"http://example.invalid\",\"click\"), <b>Bold</b> & 'Quoted'"
    assert title.startswith("<img") and isbn.startswith("<svg onload=")


@pytest.mark.parametrize("start", ["=", "+", "-", "@", "\t", "\r"])
def test_export_prefixes_every_formula_trigger(app, start):  # P1-03
    app.evaluate("""start => new Promise(resolve => {
        const book = {id: 'f1', title: start + '1+1', author: 'A', isbn: 'N/A', publishedYear: '2000', pages: 1};
        const request = db.transaction(['books'], 'readwrite').objectStore('books').add(book);
        request.onsuccess = resolve;
    })""", start)
    reload(app)
    expect(app.locator("#ledger-list li")).to_have_count(1)
    assert export_csv(app)[1][0] == "'" + start + "1+1"
