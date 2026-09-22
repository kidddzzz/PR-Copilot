# Demo Repo — Seeded Issues Reference

A small sample project with **4 deliberately planted issues**, one per
subagent (except Docs, which can flag that this README/CONTRIBUTING.md
should be checked against the code). Use this as the "PR" you run through
PR Copilot for your live demo.

| # | File | Issue | Should be caught by | Severity |
|---|---|---|---|---|
| 1 | `src/config/db.py` | Hardcoded DB password | Security agent | blocking |
| 2 | `src/auth/login.py` | Inverted login condition (logic bug) | Correctness agent | blocking |
| 3 | `src/utils/parser.py` | `parse_date()` has no unit test | Testing agent | warning |
| 4 | `src/style_offender.py` | Naming, unused import, docstrings, quote style | Style agent | warning |

## How to use this for your demo

1. Treat the current state of this repo as an open PR (e.g. diff against
   an earlier "clean" commit, or just feed these 4 files directly).
2. Run PR Copilot against it.
3. Confirm all 4 issues are caught and correctly prioritized (blocking
   issues — #1 and #2 — should surface above the warnings).
4. Time a human doing a manual review of the same 4 files for your
   before/after impact metric.

## Setup
```
pip install -r requirements.txt
pytest tests/
```
