# Shared Subagent Output Schema

Everyone building a subagent (Style, Security, Correctness, Testing, Docs) must
return findings in **this exact shape** so the Orchestration Lead can merge
them into one report without custom parsing per agent.

## Schema

```json
{
  "agent": "string",          // one of: "style" | "security" | "correctness" | "testing" | "docs"
  "status": "string",         // "ok" (no issues found) or "issues_found"
  "findings": [
    {
      "id": "string",         // unique id, e.g. "sec-001"
      "severity": "string",   // "blocking" | "warning" | "info"
      "file": "string",       // path of the file, e.g. "src/auth/login.py"
      "line": "number",       // line number the issue relates to (0 if not applicable)
      "message": "string",    // short, human-readable description of the issue
      "suggested_fix": "string" // optional: proposed fix, empty string if none
    }
  ],
  "summary": "string"         // 1-2 sentence plain-English summary from this agent
}
```

## Severity guide (use consistently across all agents)

| Severity | Meaning | Example |
|---|---|---|
| `blocking` | Must be fixed before merge | Hardcoded secret, SQL injection, broken logic |
| `warning` | Should be fixed, not merge-blocking | Missing test for a new function, style violation |
| `info` | Nice to know, no action required | Suggestion to refactor, minor doc drift |

## Example: Security Agent output

```json
{
  "agent": "security",
  "status": "issues_found",
  "findings": [
    {
      "id": "sec-001",
      "severity": "blocking",
      "file": "src/config/db.py",
      "line": 14,
      "message": "Hardcoded database password found in source code.",
      "suggested_fix": "Move credential to environment variable (DB_PASSWORD)."
    }
  ],
  "summary": "Found 1 blocking issue: hardcoded credential."
}
```

## Example: Testing Agent output

```json
{
  "agent": "testing",
  "status": "issues_found",
  "findings": [
    {
      "id": "test-001",
      "severity": "warning",
      "file": "src/utils/parser.py",
      "line": 0,
      "message": "New function 'parse_date()' has no corresponding unit test.",
      "suggested_fix": "Add a test covering valid, invalid, and empty date strings."
    }
  ],
  "summary": "Found 1 untested new function."
}
```

## Example: Style Agent output (clean case)

```json
{
  "agent": "style",
  "status": "ok",
  "findings": [],
  "summary": "No style violations found."
}
```

---

## Orchestrator merge logic (pseudocode for the Orchestration Lead)

```
1. Dispatch PR diff to all 5 subagents in parallel.
2. Wait for all 5 to return (recommended: set a timeout, e.g. 30s, so one
   slow agent doesn't block the whole pipeline. NOTE: the current
   orchestrator.py skeleton does not implement this yet — it waits
   indefinitely. Add a timeout before connecting real Bob calls.).
3. Collect all "findings" arrays into one list.
4. Sort merged list by severity: blocking > warning > info.
5. De-duplicate: if two agents flag the same (file, line), merge into
   one entry and combine their messages.
6. Build final report:
     - Count of blocking / warning / info issues
     - Full sorted findings list
     - One combined summary paragraph (can pull from each agent's "summary")
7. Post report as a PR comment (or to dashboard) via GitHub API.
```

## Rules for subagent devs

- Always return **valid JSON matching this schema**, even when no issues are found (use `"status": "ok"`, `"findings": []`).
- Use the exact `severity` values above — the orchestrator sorts on these strings, so a typo (e.g. `"Blocking"` vs `"blocking"`) breaks the merge.
- Keep `message` under ~120 characters — it needs to fit cleanly in a PR comment.
- Test your agent's output against this schema **before** the first team integration checkpoint (~hour 8-10).
