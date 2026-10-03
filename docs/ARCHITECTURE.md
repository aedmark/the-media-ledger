# Architecture

How Library Ledger fits together, for a session that has never seen it. This is the map, not the territory: it names
the parts and the rules between them, and leaves the detail to the code. Keep it short enough to read in five
minutes; update it when the shape changes (a module added, moved or merged), not for every change inside one.

Why things are this way lives in [DECISIONS.md](DECISIONS.md); this file says *what* is, and points there.

## The shape, in one paragraph

The browser loads `index.html`, which pulls Tailwind (CDN script) and the Inter font (Google Fonts) and runs one
inline `<script>`. On load the script opens IndexedDB `LibraryLedgerDB` (version 1, store `books`) and renders every
saved book. A search asks Open Library: an ISBN goes to the Books API (`/api/books`, one edition), a title and
author to `/search.json` (works, first result). `bookFromEdition()` or `bookFromWork()` turns the reply into a book
record, shown as the *staged book*. "Commit to
Ledger" writes it to IndexedDB and the in-memory `ledger` array; the bin icon deletes it; "Export CSV" builds a CSV
from the array and downloads it. Nothing else leaves the device.

## Code map

Everything is in `index.html`; these are the functions and handlers inside its `<script>`.

| Area | Where | Entry point | Talks to |
| --- | --- | --- | --- |
| Storage setup | `index.html`, top of script | `indexedDB.open(...)`, `loadLedger()` | IndexedDB |
| Search | `index.html` | `form` submit handler | Open Library; `bookFromEdition()`, `bookFromWork()`; `stageBook()` |
| Staging | `index.html` | `stageBook(book)` | the DOM |
| Saving | `index.html` | `saveBtn` click handler | IndexedDB; `updateLedgerUI()` |
| Ledger list | `index.html` | `updateLedgerUI()` | the DOM |
| Removing | `index.html` | `window.removeBook(id)` | IndexedDB; `updateLedgerUI()` |
| Export | `index.html` | `exportBtn` click handler | a Blob download |
| Notifications | `index.html` | `showToast(message, type)` | the DOM |
| Escaping | `index.html` | `escapeHTML(value)` | used by staging and the ledger list |

## Interfaces and data flow

```text
form input -> Open Library (edition or first work) -> book record -> staged book -> IndexedDB "books" + ledger[] -> list / CSV
```

| Interface | Producer | Consumer | Contract / compatibility |
| --- | --- | --- | --- |
| Book record | search handler | IndexedDB, list, CSV | `{id: string (Date.now()), title, author, isbn ('N/A' if none), publishedYear (4 chars or 'Unknown'), pages (number or 'Unknown')}`; changing it needs a migration (D-003) |
| IndexedDB `LibraryLedgerDB` v1 | `onupgradeneeded` | `loadLedger()` and handlers | store `books`, `keyPath: "id"`; no indexes |
| CSV export | export handler | the user's spreadsheet | header `Title,Author,ISBN,Published Year,Pages`; every cell double-quoted; formula-like cells start with `'` (P1-03) |
| Open Library Books API | Open Library | search handler | `{"ISBN:<isbn>": edition}` or `{}`; uses title, authors[].name, publish_date, number_of_pages, identifiers; no key (D-008) |
| Open Library search | Open Library | search handler | `docs[0]` with the requested `fields`; a work, not an edition (D-008) |

## Invariants

Rules that hold everywhere and that a change must not break. Each names what enforces it.

- Every write to the ledger goes to IndexedDB first, and `ledger[]` changes only in the request's `onsuccess`.
  Enforced by: nothing yet (P4-01).
- Nothing but the search query leaves the device. Enforced by: nothing yet; review any new `fetch` (SECURITY.md).
- Text from Open Library or storage is rendered as text, never as HTML: interpolated into `innerHTML` only
  through `escapeHTML()`, and never into inline event handlers. Enforced by: nothing automated (P4-01); manual
  injection checks in TESTING.md (P1-02).

## Boundaries

| Boundary | Comes in as | Checked by | Rule |
| --- | --- | --- | --- |
| Form fields | strings | trimmed (ISBN: `-` and spaces stripped); every value `encodeURIComponent` | encode before putting into a URL (P1-05) |
| Open Library reply | JSON | only the presence of the edition or `docs` | every string escaped with `escapeHTML()` before display (P1-02) |
| Stored records | objects from IndexedDB | nothing | same as the API reply: they came from it |
| CSV cells | strings | `csvCell()`: quotes doubled; a leading `=`, `+`, `-`, `@`, tab, or CR gets an apostrophe | no cell runs as a formula (P1-03) |

## Dependencies

Everything the project needs that it did not write. Propose a new one; it needs maintainer approval (D-004).
Record it here, pinned, the same session.

| Dependency | Version | For | Why this one (and not writing it) |
| --- | --- | --- | --- |
| Tailwind CSS Play CDN | unpinned (`cdn.tailwindcss.com`) | all styling | no build step (D-001); Tailwind marks the Play CDN as not for production, so pinning or a built stylesheet is a candidate proposal |
| Inter (Google Fonts) | weights 300, 400, 600, 800 | typography | appearance only; the page falls back to sans-serif |
| pytest, pytest-playwright, Playwright (development only) | pinned in `requirements-dev.txt` | `tests/` | drive real browsers headless; Python matches the existing tooling (D-007) |
| Open Library APIs | unversioned | book lookup | free, keyless, CORS-enabled; Google's keyless quota is 0 (D-008) |

## State and caches

| What | Where | Written by | Reset by | Committed? |
| --- | --- | --- | --- | --- |
| The user's ledger | IndexedDB `LibraryLedgerDB`, per browser and per origin | the app | browser devtools (Application > IndexedDB) or clearing site data; the app has no reset | no |
| Exported CSV | the user's downloads folder | the export button | the user | no |
| Development virtualenv | `.venv/` | `pip install -r requirements-dev.txt` | delete the folder | no, gitignored |
| Playwright browsers (about 650 MB) | `~/.cache/ms-playwright/`, shared between projects | `playwright install` | by hand only; other projects may use them | no |
| Test fixtures | `tests/fixtures/open_library/` | by hand or `tools/record_fixtures.py` | re-recording overwrites four of them | yes |

## Failure modes and observability

| Failure | User-visible behaviour | Detection | Recovery / runbook |
| --- | --- | --- | --- |
| IndexedDB unavailable or blocked | error toast "Failed to connect to local database"; saving then throws because `db` is undefined | console error | none; the user must allow site storage |
| Network down | toast "Network error while communicating with the API." | console error | retry |
| Open Library rate limit (429) | toast says searches are being limited; try again in a minute | `console.error` with the status | wait |
| Other Open Library HTTP error | toast names the HTTP status | `console.error` with the status | retry later |
| Tailwind CDN unreachable | page renders unstyled but works | none | none |

Logging is `console.error` only; it may include API error objects but never contains secrets (there are none).

## Claims vs. code

- A title search saves the ISBN of one edition of the work and the work's first publication year, not the details of
  a particular copy (D-008).
- Vercel builds preview deployments for pull requests, but no file here configures it; production is unknown (Q-004).
- The repository is called `the-media-ledger`, but only books are supported so far (D-006, P5-01).
