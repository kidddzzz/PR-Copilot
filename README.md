# PR Copilot — Pre-Bob Prep Kit

Everything here is built and tested WITHOUT IBM Bob 2.0 access, so your
team can start immediately and swap in real Bob calls the moment access
opens up.

## Folders

- **`demo-repo/`** — Sample project with 4 seeded issues (security,
  correctness, testing, style) to use for your live demo and impact
  metrics. See `demo-repo/README.md` for the full breakdown.

- **`orchestrator/`** — The Orchestration Lead's pipeline skeleton:
  - `schema.py` — validates subagent output against the shared format
  - `mock_agents.py` — placeholder subagents matching the seeded demo
    repo issues (5 findings across style, security, correctness, testing,
    docs)
  - `orchestrator.py` — the full trigger → dispatch (parallel) → collect
    → merge → output pipeline. Run it now: `python orchestrator.py`

## Verified working right now

Running `python orchestrator.py` in `orchestrator/` already produces a
complete, correctly-prioritized PR review comment from mock data — 2
blocking issues, 2 warnings, 1 info, sorted and deduplicated. This proves
the pipeline shape is sound before a single Bob call has been made.

## What to do once Bob 2.0 access opens up

1. Each subagent dev replaces the matching function body in
   `mock_agents.py` (`run_style_agent`, `run_security_agent`, etc.) with a
   real Bob 2.0 agent-mode call — keeping the same return shape.
2. The Orchestration Lead swaps `get_pr_diff()` and `post_report()` in
   `orchestrator.py` for real GitHub API calls (once the Docs/Integration
   Dev's API piece is ready) instead of the current placeholders.
3. Re-run `orchestrator.py` against a real PR from `demo-repo/` to confirm
   the swap didn't break anything.
4. Everything else (merge logic, severity sorting, dedup, schema
   validation) stays exactly as-is.

## Still to build (not started here)

- Real GitHub webhook / API integration (Docs/Integration Dev)
- Real Bob 2.0 calls inside each mock_agents.py function
- Before/after timing benchmark for your impact metric (Demo/Metrics Lead)
- Pitch deck / video / submission packaging

test
