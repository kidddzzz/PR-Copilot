"""Validation helpers for the shared subagent output schema.

Every subagent (style, security, correctness, testing, docs) must return
a dict matching this shape. See subagent-output-schema.md for the full
spec and examples.
"""

VALID_AGENTS = {"style", "security", "correctness", "testing", "docs"}
VALID_SEVERITIES = {"blocking", "warning", "info"}
SEVERITY_ORDER = {"blocking": 0, "warning": 1, "info": 2}


class SchemaError(Exception):
    """Raised when a subagent's output doesn't match the shared schema."""


def validate_agent_output(output: dict) -> None:
    """Raise SchemaError if `output` doesn't match the shared schema.

    Call this on every subagent response before it enters the merge step,
    so a malformed agent fails loudly and early instead of silently
    breaking the final report.
    """
    if output.get("agent") not in VALID_AGENTS:
        raise SchemaError(f"Invalid or missing 'agent': {output.get('agent')!r}")

    if output.get("status") not in {"ok", "issues_found"}:
        raise SchemaError(f"Invalid or missing 'status': {output.get('status')!r}")

    findings = output.get("findings")
    if not isinstance(findings, list):
        raise SchemaError("'findings' must be a list")

    for f in findings:
        if f.get("severity") not in VALID_SEVERITIES:
            raise SchemaError(f"Invalid severity in finding: {f.get('severity')!r}")
        for required in ("id", "file", "line", "message"):
            if required not in f:
                raise SchemaError(f"Finding missing required field '{required}': {f}")

    if not isinstance(output.get("summary"), str):
        raise SchemaError("'summary' must be a string")
