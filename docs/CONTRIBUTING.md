# Contributing

Use this file for the workflow shared by human and automated contributors. Agent-specific standing instructions are
in [AGENTS.md](../AGENTS.md).

## Before changing code

1. Read the README, relevant roadmap item, architecture section, and test guidance.
2. Setup: a browser and Python 3 to run the app; for tests, see [TESTING.md](TESTING.md), "Before any run".
3. Check `git status` and confirm that your change will not overlap unrelated work.
4. Mark the roadmap item `[~]` with your name and the date if the work spans sessions.
5. For a change to stored data or a split of `index.html`, agree on scope with the maintainer first.

## Make the change

- Keep each change reviewable and focused on one outcome.
- Preserve existing users' ledgers unless an accepted decision explicitly allows a break.
- Add a check for changed behaviour (TESTING.md). Make it fail for the intended reason before trusting it.
- Update documentation according to [the documentation triggers](README.md#update-triggers).
- Do not include credentials, personal data, an exported ledger, or IDE configuration (`.idea/`).

## Verify

```bash
python3 tools/check_docs.py
.venv/bin/python -m pytest -q
```

First-time setup is in [TESTING.md](TESTING.md), "Before any run"; CI runs the same two commands on every pull
request. Report the exact checks run and any checks skipped; a
partial pass is not a full pass.

## Submit and review

1. Branch from `main` as `<type>/<topic>` (`fix/`, `feat/`, `docs/`, `chore/`).
2. Commit with an imperative subject, prefixed with the roadmap ID when there is one.
3. Push and open a pull request against `main` describing what changed, the roadmap ID, the checks run and their
   results, and anything not verified.
4. The maintainer reviews and merges (squash or merge commit, their choice). Nobody else merges to `main`.
5. Releases are annotated tags `vMAJOR.MINOR.PATCH` cut by the maintainer on `main` (D-005).

A change is ready when its scope is clear, relevant checks pass, user and migration impact is described, sensitive
data is absent, and the documentation it invalidated has been updated.

## Compatibility and migrations

Saved ledgers must keep loading. A change to the database name, store, or record shape must bump the IndexedDB
version, migrate version-1 data in `onupgradeneeded`, add a decision superseding D-003, and be verified with the
migration check in TESTING.md. CSV export columns may gain columns at the end; renaming or reordering is a user-visible
change for the CHANGELOG.

## Reporting security issues

Do not open a public issue for a suspected vulnerability. Follow [SECURITY.md](SECURITY.md).
