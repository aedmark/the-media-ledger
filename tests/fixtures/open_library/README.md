# Open Library replies used by the tests

The tests never call Open Library: `tests/conftest.py` answers every request to `openlibrary.org` from these files.

| File | Answers | Source |
| --- | --- | --- |
| `isbn_9780439708180.json` | Books API, `ISBN:9780439708180` | recorded 2026-10-03 |
| `isbn_not_found.json` | Books API, any other ISBN | recorded 2026-10-03 (ISBN `9798888888884`) |
| `search_dune_frank_herbert.json` | search, title `Dune`, author `Frank Herbert` | recorded 2026-10-03 |
| `search_empty.json` | search, any other title | recorded 2026-10-03 |
| `search_isbn10_first.json` | search, a work whose first ISBN is an ISBN-10 | synthetic: pins the ISBN-13 preference |
| `search_no_isbn.json` | search, a work without ISBNs | synthetic: Open Library cannot be made to return it on demand |
| `search_hostile.json` | search, HTML and spreadsheet formulas in every text field | synthetic: an attack fixture |

Recorded replies are trimmed to the fields the app reads (and a work's ISBN list to its first 10), so they stay small
and stable. To refresh them, run `python3 tools/record_fixtures.py`, review the diff, update the dates here, and rerun
the tests: a test that now fails has found a change in Open Library's data or shape.
