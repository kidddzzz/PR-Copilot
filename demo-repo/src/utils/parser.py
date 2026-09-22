"""Date/string parsing utilities.

SEEDED ISSUE (testing, warning):
`parse_date` is a new function added in this "PR" with no corresponding
unit test in tests/. The Testing subagent should flag this as a coverage
gap and suggest test cases (valid date, invalid date, empty string).
"""

from datetime import datetime


def parse_date(raw: str):
    """Parse a date string in YYYY-MM-DD format.

    No unit test currently exists for this function -- seeded gap for
    the Testing subagent to catch.
    """
    return datetime.strptime(raw, "%Y-%m-%d")


def normalize_whitespace(text: str) -> str:
    """Collapse repeated whitespace into single spaces. (Has a test.)"""
    return " ".join(text.split())
