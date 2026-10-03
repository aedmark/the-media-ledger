# Roadmap

Item IDs are permanent: `P<phase>-<nn>`. Never renumber; append new items at the end of their phase.
`[ ]` open · `[~]` in progress (who holds it, since when, and what is left) · `[x]` done · `[-]` dropped (say why,
and the decision). An item held `[~]` by someone else is theirs until they or a maintainer release it.

A finished item says what was done, the decision if any, the evidence (the test, or the measurement), and the date.
A new item says where it came from (a test run, a real user, a maintainer) and the date. Keep an item's history in it:
"tried X, measured Y, then did Z" is how the next session avoids trying X again. Bugs are items too, filed under
the phase they belong to.

If an external issue tracker is the project's source of truth, replace this file with a short link and document the
tracker's ID and status conventions. Do not maintain two competing roadmaps.

## Phase 1: {{Foundations}}

Goal: {{one sentence}}

- [ ] P1-01 {{Item: what, and how you will know it is done}}
- [ ] P1-02 {{Item}}

## Phase 2: {{Core experience}}

Goal: {{one sentence}}

- [ ] P2-01 {{Item}}

## Phase 3: {{Output / sharing}}

- [ ] P3-01 {{Item}}

## Phase 4: {{Quality: speed, accessibility, robustness}}

- [ ] P4-01 {{Item}}

## Phase 5: {{Later / only if wanted}}

Not committed. Decide only after the phases above ship.

- [ ] P5-01 {{Item}}

## Phase 6: {{Non-code items (name, domain, brand)}}

- [ ] P6-01 {{Item}}

<!-- Examples of finished, in-progress and dropped items:
- [x] P3-02 Import files by picker and drag-and-drop (D-016: each file becomes a new item; nothing is overwritten).
  Three end-to-end checks, each failing without the fix (2026-05-02)
- [~] P2-07 Retry a rejected plan (Codex, since 2026-05-08). Done for validation errors; left: runtime errors (P2-18). Found by the harness,
  task C2, 4 of 7 runs (2026-05-09)
- [-] P3-11 A hand-written PDF writer (dropped, D-050: printing to PDF through the browser is enough)
-->
