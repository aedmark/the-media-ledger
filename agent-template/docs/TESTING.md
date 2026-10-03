# Testing

How to run every test, what each one proves, and what it cannot. Read this before claiming anything works.
The results themselves live in HANDOFF's "Current state"; this file is how to get them.

## The suites

| Suite | File | Proves | Does not prove | Time, needs |
| --- | --- | --- | --- | --- |
| {{Structure}} | `{{test/structure.js}}` | {{every file is registered; every module has its required parts}} | {{that anything runs}} | {{seconds, no browser}} |
| {{Unit}} | `{{test/unit}}` | {{parser rules, pure functions}} | {{the UI, real storage}} | {{seconds}} |
| {{End to end}} | `{{test/e2e.js}}` | {{a user's path through the app in headless Chromium}} | {{Firefox, Safari, a real phone}} | {{a minute, a browser}} |
| {{Against a real service / model}} | `{{test/live.js}}` | {{the integration works today}} | {{that it works every time (see "Runs that vary")}} | {{minutes, the service}} |

**The fast set** (before every commit): `{{command}}`, `{{command}}`.
**The full set** (after deleting or moving code, and before a release): all of the above.

**Expected results** live in HANDOFF's "Verified" table, with the date and commit they were measured on. A count
written anywhere else (a comment, a command's `# expect 633 passed`) goes stale without anyone noticing: point to
HANDOFF instead.

## Before any run

What has to be true before a test or a real run means anything, and what keeps a run from harming the machine.

- **Clean state:** {{the reset command, e.g. `sh reset.sh`}}. Tests and runs read {{saves, logs, learned data}}; a
  leftover from an earlier run can pass or fail a test for the wrong reason. The reset must not delete
  {{caches that are expensive to rebuild}} (ARCHITECTURE, "State and caches").
- **Resource caps:** {{e.g. "run the suite under `systemd-run --user --scope -p MemoryMax=8G`"}}. A runaway test (a
  mock that grows forever, a loop against a model) can take the whole machine, and the session with it.
- **Services it needs:** {{a local model server, a dev server on port NNNN}}, and how to tell they are up.

## Running each suite

### {{Suite name}}

```bash
{{exact command, including any server it needs, with the port}}
```

- What it does, in order: {{...}}
- What a pass looks like: {{the final line, the exit code}}. {{A run that aborts partway can print many PASS lines
  and no summary: check for the abort, not only for FAIL.}}
- Where it writes its output: {{path}}; {{gitignored? overwritten each run?}}
- Options: {{environment variables, e.g. run a subset, a timeout}}.

### Adding a check

- {{Where new checks go and the helper to use.}}
- Assert on what happened (a file on disk, a returned value), not on words in a message: a message can mention the
  right word for the wrong reason.
- Before trusting a new check, make it fail: undo the fix (only the fix) and run it. A check that passes either way
  proves nothing.

## Runs that vary

{{Delete this section if nothing in the project is nondeterministic.}}

Some results depend on something outside the code: a language model, the network, timing under load. For those:

- **One run proves little.** Run it several times and record the tally with the date and what varied
  ("6/7, 7/7, 5/7 on {{model}}, 2026-..-..").
- **Read the failure before blaming the code.** Say in the handoff whether a miss was the code or the outside thing.
- **To test how the code handles a rare bad input**, inject it (replace the first reply, delay one request)
  rather than rerunning until it happens.
- **Measure one case in isolation** when that is what changed, with an option that runs a subset.
- **Check the judge before trusting its verdict.** Anything that scores output (a model as judge, a similarity
  metric, a rubric) gets controls first: cases with a known right answer, including a deliberately bad one it must
  rank last. A judge that fails its controls is not evidence, however good the real results look; record the control
  results next to the verdict.

## Change-to-check matrix

| Changed area | Minimum checks | Additional evidence |
| --- | --- | --- |
| {{Documentation only}} | `python3 tools/check_docs.py` | {{render or link check if relevant}} |
| {{Pure logic}} | {{unit suite}} | {{property, fuzz, or mutation check for critical rules}} |
| {{User workflow}} | {{unit plus end-to-end}} | {{manual accessibility or device check}} |
| {{Schema, migration, or persistence}} | {{migration and integration suites}} | {{backup/rollback rehearsal}} |
| {{Security boundary}} | {{negative and abuse-case tests}} | {{targeted security review}} |

## Manual checks (before a release)

What only a person can check, and how. Record who checked what, where and when in HANDOFF.

- {{e.g. "Open each app; type, save, reload; check nothing is lost."}}
- {{Browsers and devices that are supported but not automated.}}

## Environment recipes

{{How to get the test tools in each environment (AGENTS.md, "Environments"): e.g. "Playwright is
not installed globally: `npm i playwright@1.56` in a scratch directory, then `NODE_PATH` to it and `CHROME` to the
system browser."}}

## Known pitfalls (already hit, already fixed: don't re-discover these)

- {{The trap, the symptom it produced, and what to do instead. Add one each time a session loses time to something
  a future session could also hit.}}
- **A mutation check must break the fix, not the test.** Reverting a whole file can fail a test for an unrelated
  reason. Remove just the fix.
- **A test that calls internals breaks when they are cleaned up.** Call what the app calls (its public entry
  point), and rerun the full set after deleting code.
