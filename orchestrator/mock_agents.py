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
    """TODO: replace with real Bob 2.0 call. Mirrors style_offender.py.

    Checks against rules in CONTRIBUTING.md:
      - snake_case for functions and parameters
      - Every public function must have a docstring
      - No unused imports
      - Use double quotes consistently
    """
    return {
        "agent": "style",
        "status": "issues_found",
        "findings": [
            # style-001 (CalculateTotal not snake_case) removed:
            # function was renamed to 'snake_case' — naming violation resolved.
            {
                "id": "style-002",
                "severity": "warning",
                "file": "src/style_offender.py",
                "line": 10,
                "message": "Parameter name 'itemList' should be snake_case (CONTRIBUTING.md: Naming conventions).",
                "suggested_fix": "Rename parameter to 'item_list'.",
            },
            {
                "id": "style-003",
                "severity": "warning",
                "file": "src/style_offender.py",
                "line": 10,
                "message": "Public function 'calculate_total' has no docstring (CONTRIBUTING.md: Docstrings).",
                "suggested_fix": "Add a docstring describing what the function does, e.g. \"\"\"Return the total price for all items in item_list.\"\"\"",
            },
            {
                "id": "style-004",
                "severity": "warning",
                "file": "src/style_offender.py",
                "line": 13,
                "message": "Single quotes used for dict key access: i['price'], i['qty'] (CONTRIBUTING.md: Strings).",
                "suggested_fix": "Use double quotes: i[\"price\"], i[\"qty\"].",
            },
            {
                "id": "style-005",
                "severity": "warning",
                "file": "src/style_offender.py",
                "line": 17,
                "message": "Parameter name 'Name' should be lowercase snake_case (CONTRIBUTING.md: Naming conventions).",
                "suggested_fix": "Rename parameter to 'name'.",
            },
            {
                "id": "style-006",
                "severity": "warning",
                "file": "src/style_offender.py",
                "line": 17,
                "message": "Public function 'get_greeting' has no docstring (CONTRIBUTING.md: Docstrings).",
                "suggested_fix": "Add a docstring, e.g. \"\"\"Return a greeting string for the given name.\"\"\"",
            },
            {
                "id": "style-007",
                "severity": "warning",
                "file": "src/style_offender.py",
                "line": 18,
                "message": "Mixed quote styles: 'Hello, ' uses single quotes alongside double-quoted \"!\" (CONTRIBUTING.md: Strings).",
                "suggested_fix": "Use double quotes consistently: \"Hello, \" + name + \"!\"",
            },
            {
                "id": "style-008",
                "severity": "info",
                "file": "src/style_offender.py",
                "line": 8,
                "message": "Unused import 'sys' - never referenced in this file (CONTRIBUTING.md: Imports).",
                "suggested_fix": "Remove the unused import.",
            },
        ],
        "summary": (
            "Found 7 style issues: 1 camelCase parameter, 2 missing docstrings, "
            "2 quote-style violations, 1 capitalised parameter, and 1 unused import."
        ),
    }


def run_security_agent(pr_diff: str) -> dict:
    """TODO: replace with real Bob 2.0 call. Mirrors src/config/db.py.

    Scans for:
      - Hardcoded credentials / secrets  → blocking
      - Hardcoded internal infrastructure details (host, user, db name)
        that leak topology / account info to anyone with repo access → warning
      - Injection risks via psycopg2 named params → none found (safe)
    """
    return {
        "agent": "security",
        "status": "issues_found",
        "findings": [
            {
                "id": "sec-001",
                "severity": "blocking",
                "file": "src/config/db.py",
                "line": 14,
                "message": (
                    "Hardcoded plaintext password 'SuperSecret123!' assigned to DB_PASSWORD. "
                    "Anyone with read access to the repo obtains the production database credential."
                ),
                "suggested_fix": (
                    "Replace with os.environ[\"DB_PASSWORD\"] and document the required "
                    "environment variable in the deployment guide."
                ),
            },
            {
                "id": "sec-002",
                "severity": "warning",
                "file": "src/config/db.py",
                "line": 13,
                "message": (
                    "Hardcoded service account username 'app_service' assigned to DB_USER. "
                    "Leaks the exact account name an attacker should target for credential stuffing."
                ),
                "suggested_fix": "Replace with os.environ[\"DB_USER\"].",
            },
            {
                "id": "sec-003",
                "severity": "warning",
                "file": "src/config/db.py",
                "line": 12,
                "message": (
                    "Hardcoded internal hostname 'prod-db.internal.example.com' assigned to DB_HOST. "
                    "Exposes internal network topology to anyone with repo read access."
                ),
                "suggested_fix": "Replace with os.environ[\"DB_HOST\"].",
            },
            {
                "id": "sec-004",
                "severity": "warning",
                "file": "src/config/db.py",
                "line": 15,
                "message": (
                    "Hardcoded production database name 'app_production' assigned to DB_NAME. "
                    "Confirms this is a live production system and assists reconnaissance."
                ),
                "suggested_fix": "Replace with os.environ[\"DB_NAME\"].",
            },
        ],
        "summary": (
            "Found 4 security issues in src/config/db.py: 1 blocking (hardcoded password) "
            "and 3 warnings (hardcoded host, username, and database name leaking "
            "production infrastructure details)."
        ),
    }


def run_correctness_agent(pr_diff: str) -> dict:
    """TODO: replace with real Bob 2.0 call. Mirrors src/auth/login.py.

    Traces the full call chain:
      login() -> is_valid_login() -> bool
    Checks for: inverted conditions, off-by-one errors, edge cases (None/empty
    input), and contract mismatches between docstring and implementation.
    """
    return {
        "agent": "correctness",
        "status": "issues_found",
        "findings": [
            {
                "id": "corr-001",
                "severity": "blocking",
                "file": "src/auth/login.py",
                "line": 16,
                "message": (
                    "Inverted condition in is_valid_login(): uses '!=' so it returns True "
                    "when passwords do NOT match and False when they do. "
                    "login() calls this directly - every wrong password is accepted and "
                    "every correct password is rejected."
                ),
                "suggested_fix": (
                    "Replace the if/return block with: "
                    "return stored_password_hash == provided_password_hash"
                ),
            },
            {
                "id": "corr-002",
                "severity": "warning",
                "file": "src/auth/login.py",
                "line": 10,
                "message": (
                    "is_valid_login() has no guard for empty or None inputs. "
                    "If stored_password_hash is None or '' the comparison silently "
                    "returns False instead of raising - an account with no stored hash "
                    "appears to have a login failure rather than a configuration error. "
                    "If provided_password_hash is '' it could match an empty stored hash."
                ),
                "suggested_fix": (
                    "Add an early guard: "
                    "if not stored_password_hash or not provided_password_hash: return False"
                ),
            },
            {
                "id": "corr-003",
                "severity": "warning",
                "file": "src/auth/login.py",
                "line": 10,
                "message": (
                    "No unit tests exist for is_valid_login() or login(). "
                    "A basic test (correct hash -> True, wrong hash -> False) would have "
                    "caught the inverted condition immediately."
                ),
                "suggested_fix": (
                    "Add tests: assert is_valid_login('h', 'h') is True, "
                    "assert is_valid_login('h', 'x') is False, "
                    "assert is_valid_login('', 'h') is False, "
                    "assert is_valid_login(None, 'h') is False."
                ),
            },
        ],
        "summary": (
            "Found 3 correctness issues in src/auth/login.py: 1 blocking (inverted "
            "condition lets any wrong password through) and 2 warnings (no None/empty "
            "input guard, no unit tests)."
        ),
    }


def run_testing_agent(pr_diff: str) -> dict:
    """TODO: replace with real Bob 2.0 call. Mirrors src/utils/parser.py.

    Checks every new/modified function in the diff against tests/.
    - normalize_whitespace: covered by 2 existing tests. No gap.
    - parse_date: new function, zero tests found anywhere. Gap reported.
    """
    return {
        "agent": "testing",
        "status": "issues_found",
        "findings": [
            {
                "id": "test-001",
                "severity": "warning",
                "file": "src/utils/parser.py",
                "line": 12,
                "message": (
                    "New function 'parse_date()' has no corresponding unit test in tests/. "
                    "normalize_whitespace() in the same file has 2 tests, so this is a "
                    "deliberate gap, not a repo-wide habit."
                ),
                "suggested_fix": (
                    "Add the following 5 tests to tests/test_parser.py: "
                    "(1) valid input: parse_date('2024-06-15') returns datetime(2024,6,15); "
                    "(2) wrong format: parse_date('15-06-2024') raises ValueError; "
                    "(3) empty string: parse_date('') raises ValueError; "
                    "(4) impossible date: parse_date('2023-02-29') raises ValueError; "
                    "(5) None input: parse_date(None) raises TypeError."
                ),
            },
        ],
        "summary": (
            "Found 1 untested new function: parse_date() in src/utils/parser.py. "
            "Suggested 5 concrete test cases covering valid input, wrong format, "
            "empty string, impossible date, and None."
        ),
    }


def run_docs_agent(pr_diff: str) -> dict:
    """TODO: replace with real Bob 2.0 call. Produces the plain-English PR summary.

    Checks:
      - README.md claims vs. actual code state
      - CONTRIBUTING.md rules vs. what the PR introduces
    """
    return {
        "agent": "docs",
        "status": "issues_found",
        "findings": [
            {
                "id": "docs-001",
                "severity": "info",
                "file": "demo-repo/README.md",
                "line": 13,
                "message": (
                    "README answer-key table row 4 describes src/style_offender.py as "
                    "'Naming, unused import, docstrings, quote style' — 4 categories — "
                    "but the file currently contains 7 distinct violations "
                    "(1 camelCase param 'itemList', 1 capitalised param 'Name', "
                    "2 missing docstrings, 2 quote-style violations, 1 unused import). "
                    "The function-name violation was resolved when 'CalculateTotal' was renamed to 'calculate_total'. "
                    "A reviewer comparing the table to the pipeline output will see a count mismatch."
                ),
                "suggested_fix": (
                    "Update the table cell to: "
                    "'7 violations: camelCase param, capitalised param, missing docstrings (x2), "
                    "mixed quotes (x2), unused import'."
                ),
            },
            {
                "id": "docs-002",
                "severity": "warning",
                "file": "demo-repo/CONTRIBUTING.md",
                "line": 26,
                "message": (
                    "CONTRIBUTING.md Testing rule states: 'Every new function should have "
                    "at least one corresponding unit test in tests/'. "
                    "This PR introduces parse_date() in src/utils/parser.py with zero tests — "
                    "the code drifted from the documented requirement. "
                    "The rule itself is not outdated; the PR is non-compliant with it."
                ),
                "suggested_fix": (
                    "Add tests/test_parser.py with tests for parse_date() before merging, "
                    "or update CONTRIBUTING.md to note that parse_date() is an acknowledged exception."
                ),
            },
        ],
        "summary": (
            "This PR adds a parse_date() utility, hardens DB config, updates login validation, "
            "and refactors style helpers — touching 4 files across auth, config, utilities, and style. "
            "2 documentation findings: README issue-count understates style violations (info), "
            "and parse_date() ships without a test in violation of CONTRIBUTING.md's Testing rule (warning)."
        ),
    }


ALL_AGENTS = [
    run_style_agent,
    run_security_agent,
    run_correctness_agent,
    run_testing_agent,
    run_docs_agent,
]
