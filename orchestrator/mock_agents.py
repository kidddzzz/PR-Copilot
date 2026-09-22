"""Mock subagents.

These stand in for real IBM Bob 2.0 subagent calls so the Orchestration
Lead (and the rest of the team) can build and test the full pipeline
BEFORE Bob 2.0 access is available. Each function returns output matching
the shared schema (see schema.py / subagent-output-schema.md) and mirrors
the issues seeded in demo-repo/.

Once Bob 2.0 is available, replace the body of each function with an
actual call to Bob (agent mode / subagent), keeping the same return shape
so nothing downstream (the merge/orchestration logic) needs to change.
"""


def run_style_agent(pr_diff: str) -> dict:
    """TODO: replace with real Bob 2.0 call. Mirrors style_offender.py."""
    return {
        "agent": "style",
        "status": "issues_found",
        "findings": [
            {
                "id": "style-001",
                "severity": "warning",
                "file": "src/style_offender.py",
                "line": 10,
                "message": "Function name 'CalculateTotal' should be snake_case.",
                "suggested_fix": "Rename to 'calculate_total'.",
            },
            {
                "id": "style-002",
                "severity": "info",
                "file": "src/style_offender.py",
                "line": 8,
                "message": "Unused import 'sys'.",
                "suggested_fix": "Remove the unused import.",
            },
        ],
        "summary": "Found 2 style issues: naming convention and an unused import.",
    }


def run_security_agent(pr_diff: str) -> dict:
    """TODO: replace with real Bob 2.0 call. Mirrors src/config/db.py."""
    return {
        "agent": "security",
        "status": "issues_found",
        "findings": [
            {
                "id": "sec-001",
                "severity": "blocking",
                "file": "src/config/db.py",
                "line": 14,
                "message": "Hardcoded database password found in source code.",
                "suggested_fix": "Move credential to an environment variable (DB_PASSWORD).",
            },
        ],
        "summary": "Found 1 blocking issue: hardcoded credential.",
    }


def run_correctness_agent(pr_diff: str) -> dict:
    """TODO: replace with real Bob 2.0 call. Mirrors src/auth/login.py."""
    return {
        "agent": "correctness",
        "status": "issues_found",
        "findings": [
            {
                "id": "corr-001",
                "severity": "blocking",
                "file": "src/auth/login.py",
                "line": 16,
                "message": "Condition is inverted: returns True when the password does NOT match.",
                "suggested_fix": "Change 'return True' to 'return False' in the mismatch branch.",
            },
        ],
        "summary": "Found 1 blocking logic error in login validation.",
    }


def run_testing_agent(pr_diff: str) -> dict:
    """TODO: replace with real Bob 2.0 call. Mirrors src/utils/parser.py."""
    return {
        "agent": "testing",
        "status": "issues_found",
        "findings": [
            {
                "id": "test-001",
                "severity": "warning",
                "file": "src/utils/parser.py",
                "line": 0,
                "message": "New function 'parse_date()' has no corresponding unit test.",
                "suggested_fix": "Add tests for a valid date, an invalid date, and an empty string.",
            },
        ],
        "summary": "Found 1 untested new function.",
    }


def run_docs_agent(pr_diff: str) -> dict:
    """TODO: replace with real Bob 2.0 call. Produces the plain-English PR summary."""
    return {
        "agent": "docs",
        "status": "ok",
        "findings": [],
        "summary": (
            "This PR touches database config, login validation, a date parser, "
            "and adds a new utility file. No documentation drift detected."
        ),
    }


ALL_AGENTS = [
    run_style_agent,
    run_security_agent,
    run_correctness_agent,
    run_testing_agent,
    run_docs_agent,
]
