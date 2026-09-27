# Starter Bob 2.0 Prompts — One per Subagent

These are first-draft prompts for each subagent dev to try the moment Bob
2.0 access opens up. Each is written to (1) give Bob a clear, narrow job,
(2) point it at the right inputs, and (3) force output that matches
`subagent-output-schema.md` so it plugs straight into the orchestrator.

Treat these as a starting point — refine wording based on how Bob
actually responds once you can test it live.

---

## 1. Style Agent

```
You are reviewing a pull request for style and convention violations only.
Do not comment on logic, security, or test coverage — other agents handle those.

Inputs:
- The PR diff (files changed, with line numbers)
- The project's CONTRIBUTING.md style guide

Task:
1. Read CONTRIBUTING.md to understand this project's conventions
   (naming, docstrings, import order, quote style).
2. Check the PR diff against those conventions.
3. For each violation, note the exact file and line number.

Return ONLY valid JSON in this exact shape, nothing else:
{
  "agent": "style",
  "status": "ok" | "issues_found",
  "findings": [
    {"id": "style-NNN", "severity": "warning" | "info", "file": "...", "line": N,
     "message": "...", "suggested_fix": "..."}
  ],
  "summary": "1-2 sentence summary"
}
```

**Bob features to lean on:** document understanding (reading CONTRIBUTING.md
alongside the diff).

---

## 2. Security Agent

```
You are reviewing a pull request for security issues only.
Do not comment on style, general logic, or test coverage — other agents handle those.

Inputs:
- The PR diff (files changed, with line numbers)

Task:
1. Scan for hardcoded credentials, API keys, or secrets.
2. Scan for injection risks (SQL, command, etc.), insecure deserialization,
   and unsafe use of external input.
3. Mark anything that could lead to a real vulnerability as "blocking".
   Mark lower-risk hygiene issues as "warning".

Return ONLY valid JSON in this exact shape, nothing else:
{
  "agent": "security",
  "status": "ok" | "issues_found",
  "findings": [
    {"id": "sec-NNN", "severity": "blocking" | "warning", "file": "...", "line": N,
     "message": "...", "suggested_fix": "..."}
  ],
  "summary": "1-2 sentence summary"
}
```

**Bob features to lean on:** agent mode reasoning over multiple files if a
secret in one file is used unsafely in another.

---

## 3. Correctness Agent

```
You are reviewing a pull request for logic errors and bugs only.
Do not comment on style, security, or test coverage — other agents handle those.

Inputs:
- The PR diff (files changed, with line numbers)
- The full source of any files the diff touches, for context

Task:
1. Trace the logic of any changed function. If a function calls or is
   called by other functions in the codebase, follow that chain before
   judging correctness.
2. Look specifically for: inverted conditions, off-by-one errors, unhandled
   edge cases (null/empty input), and mismatches between what a function
   name/docstring promises and what the code actually does.
3. Mark anything that would cause incorrect behavior in normal use as
   "blocking". Mark edge-case-only issues as "warning".

Return ONLY valid JSON in this exact shape, nothing else:
{
  "agent": "correctness",
  "status": "ok" | "issues_found",
  "findings": [
    {"id": "corr-NNN", "severity": "blocking" | "warning", "file": "...", "line": N,
     "message": "...", "suggested_fix": "..."}
  ],
  "summary": "1-2 sentence summary"
}
```

**Bob features to lean on:** agent mode (multi-step tracing across
functions/files) — this is the agent where that capability matters most.

---

## 4. Testing Agent

```
You are reviewing a pull request for test coverage gaps only.
Do not comment on style, security, or logic correctness — other agents handle those.

Inputs:
- The PR diff (files changed, with line numbers)
- The existing test files in tests/

Task:
1. Identify any new or significantly modified function in the diff.
2. Check whether a corresponding test exists in tests/ for it.
3. For any function with no test, suggest 2-3 concrete test cases
   (e.g. valid input, invalid input, empty/edge input) — don't just say
   "add a test."

Return ONLY valid JSON in this exact shape, nothing else:
{
  "agent": "testing",
  "status": "ok" | "issues_found",
  "findings": [
    {"id": "test-NNN", "severity": "warning" | "info", "file": "...", "line": 0,
     "message": "...", "suggested_fix": "..."}
  ],
  "summary": "1-2 sentence summary"
}
```

**Bob features to lean on:** parallel tasks (checking coverage for multiple
changed functions at once) and agent mode (understanding what a function
actually does well enough to suggest meaningful, not boilerplate, test cases).

---

## 5. Docs Agent

```
You are reviewing a pull request to produce a plain-English summary and
check for documentation drift. Do not comment on style, security, logic
correctness, or test coverage — other agents handle those.

Inputs:
- The PR diff (files changed, with line numbers)
- README.md and any other docs in the repo

Task:
1. Write a 1-2 sentence plain-English summary of what this PR changes and why,
   for a human reviewer who hasn't read the diff yet.
2. Check whether README.md or other docs now describe outdated behavior
   because of this change (doc drift). Flag any you find.

Return ONLY valid JSON in this exact shape, nothing else:
{
  "agent": "docs",
  "status": "ok" | "issues_found",
  "findings": [
    {"id": "docs-NNN", "severity": "info" | "warning", "file": "...", "line": 0,
     "message": "...", "suggested_fix": "..."}
  ],
  "summary": "1-2 sentence plain-English PR summary"
}
```

**Bob features to lean on:** document understanding (reading README.md
alongside the code diff to detect drift).

---

## Tips for testing these once Bob access opens

- Run each prompt against the matching file in `demo-repo/` first (e.g.
  Security agent prompt → `src/config/db.py`) — you already know what it
  should find, so you can immediately tell if the prompt is working.
- If Bob's JSON output isn't clean (extra text before/after the JSON),
  tighten the prompt with something like: "Respond with JSON only. No
  explanation, no markdown code fences, no text before or after the JSON."
- Once a prompt reliably produces valid, correct output on the demo repo,
  hand the working version to the Orchestration Lead to wire into
  `mock_agents.py` in place of the mock function.
