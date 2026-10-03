# Architecture

How Library Ledger fits together, for a session that has never seen it. This is the map, not the territory: it names
the parts and the rules between them, and leaves the detail to the code. Keep it short enough to read in five
minutes; update it when the shape changes (a module added, moved or merged), not for every change inside one.

Why things are this way lives in [DECISIONS.md](DECISIONS.md); this file says *what* is, and points there.

## The shape, in one paragraph

The browser loads `index.html`, which pulls Tailwind (CDN script) and the Inter font (Google Fonts) and runs one
inline `<script>`. On load the script opens IndexedDB `LibraryLedgerDB` (version 1, store `books`) and renders every
saved book. A search builds a Google Books query (`isbn:` or `intitle:`/`inauthor:`), fetches
`https://www.googleapis.com/books/v1/volumes`, takes the first result, and shows it as the *staged book*. "Commit to
Ledger" writes it to IndexedDB and the in-memory `ledger` array; the bin icon deletes it; "Export CSV" builds a CSV
from the array and downloads it. Nothing else leaves the device.

## Code map

Everything is in `index.html`; these are the functions and handlers inside its `<script>`.

| Area | Where | Entry point | Talks to |
| --- | --- | --- | --- |
| Storage setup | `index.html`, top of script | `indexedDB.open(...)`, `loadLedger()` | IndexedDB |
| Search | `index.html` | `form` submit handler | Google Books API; `stageBook()` |
| Staging | `index.html` | `stageBook(book)` | the DOM |
| Saving | `index.html` | `saveBtn` click handler | IndexedDB; `updateLedgerUI()` |
| Ledger list | `index.html` | `updateLedgerUI()` | the DOM |
| Removing | `index.html` | `window.removeBook(id)` | IndexedDB; `updateLedgerUI()` |
| Export | `index.html` | `exportBtn` click handler | a Blob download |
| Notifications | `index.html` | `showToast(message, type)` | the DOM |

## Interfaces and data flow

```text
form input -> Google Books query -> first volume -> staged book -> IndexedDB "books" + ledger[] -> list / CSV
```

| Interface | Producer | Consumer | Contract / compatibility |
| --- | --- | --- | --- |
| Book record | search handler | IndexedDB, list, CSV | `{id: string (Date.now()), title, author, isbn ('N/A' if none), publishedYear (4 chars or 'Unknown'), pages (number or 'Unknown')}`; changing it needs a migration (D-003) |
| IndexedDB `LibraryLedgerDB` v1 | `onupgradeneeded` | `loadLedger()` and handlers | store `books`, `keyPath: "id"`; no indexes |
| CSV export | export handler | the user's spreadsheet | header `Title,Author,ISBN,Published Year,Pages`; every cell double-quoted |
| Google Books volumes | Google | search handler | uses `items[0].volumeInfo` only; no API key (D-002) |

## Invariants

Rules that hold everywhere and that a change must not break. Each names what enforces it.

- Every write to the ledger goes to IndexedDB first, and `ledger[]` changes only in the request's `onsuccess`.
  Enforced by: nothing yet (P4-01).
- Nothing but the search query leaves the device. Enforced by: nothing yet; review any new `fetch` (SECURITY.md).
- Text from Google Books or storage is rendered as text, never as HTML. **Currently broken** (P1-02).

## Boundaries

| Boundary | Comes in as | Checked by | Rule |
| --- | --- | --- | --- |
| Form fields | strings | trimmed; title/author `encodeURIComponent`, ISBN only strips `-` and spaces | encode before putting into a URL (P1-05) |
| Google Books reply | JSON | only `totalItems`/`items` presence | treat every string as untrusted; escape before display (P1-02) |
| Stored records | objects from IndexedDB | nothing | same as the API reply: they came from it |
| CSV cells | strings | quotes doubled | must not start a formula (P1-03) |

## Dependencies

Everything the project needs that it did not write. Propose a new one; it needs maintainer approval (D-004).
Record it here, pinned, the same session.

| Dependency | Version | For | Why this one (and not writing it) |
| --- | --- | --- | --- |
| Tailwind CSS Play CDN | unpinned (`cdn.tailwindcss.com`) | all styling | no build step (D-001); Tailwind marks the Play CDN as not for production, so pinning or a built stylesheet is a candidate proposal |
| Inter (Google Fonts) | weights 300, 400, 600, 800 | typography | appearance only; the page falls back to sans-serif |
| Google Books API v1 | v1 | book lookup | free, CORS-enabled, no key needed (D-002) |

## State and caches

| What | Where | Written by | Reset by | Committed? |
| --- | --- | --- | --- | --- |
| The user's ledger | IndexedDB `LibraryLedgerDB`, per browser and per origin | the app | browser devtools (Application > IndexedDB) or clearing site data; the app has no reset | no |
| Exported CSV | the user's downloads folder | the export button | the user | no |

## Failure modes and observability

| Failure | User-visible behaviour | Detection | Recovery / runbook |
| --- | --- | --- | --- |
| IndexedDB unavailable or blocked | error toast "Failed to connect to local database"; saving then throws because `db` is undefined | console error | none; the user must allow site storage |
| Network down | toast "Network error while communicating with the API." | console error | retry |
| Google Books HTTP error or rate limit | toast "No books found for this query." (misleading) | none | P1-05 |
| Tailwind CDN unreachable | page renders unstyled but works | none | none |

Logging is `console.error` only; it may include API error objects but never contains secrets (there are none).

## Claims vs. code

- The ledger subtitle says "In-memory session storage"; data actually persists in IndexedDB (P1-04).
- The page title says "Zero-Dependency Book Tracker"; it depends on two CDNs and the Google Books API (P1-04).
- The repository is called `the-media-ledger`, but only books are supported so far (D-006, P5-01).
