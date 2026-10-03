# Library Ledger

A small book tracker that lives in one HTML file. Look a book up by ISBN or by title and author, save it to your
ledger, and export the ledger as a CSV spreadsheet. Your ledger is stored in your browser (IndexedDB) and never
leaves your device; only the search itself goes to the Google Books API.

## Run it

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/>. Opening `index.html` directly also works, but the browser keeps a separate ledger
for `file://` pages, so stick to one way of opening it.

## Use it

1. Choose **ISBN** or **Title & Author**, fill in the fields, and press **Search Database**.
2. Check the result under **Ready to Save** and press **Commit to Ledger**.
3. Remove an entry with its bin icon; download everything with **Export CSV**.

## Develop it

Start with [AGENTS.md](AGENTS.md) (rules for humans and coding agents alike), then
[docs/HANDOFF.md](docs/HANDOFF.md) for where things stand and [ROADMAP.md](ROADMAP.md) for what is next. The
documentation map is [docs/README.md](docs/README.md).

Tests run headless in Chromium and Firefox without touching the network:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m playwright install chromium-headless-shell firefox
.venv/bin/python -m pytest -q
```

## Licence

MIT, see [LICENSE](LICENSE).
