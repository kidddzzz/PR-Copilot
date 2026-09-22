"""PR Copilot orchestrator skeleton.

Implements the 5-step pipeline: trigger -> dispatch -> collect -> merge -> output.
Currently wired to mock_agents.py so the whole flow can be built and tested
BEFORE IBM Bob 2.0 access is available. Swap mock_agents functions for real
Bob 2.0 agent-mode / subagent calls once access opens up -- the merge logic
below does not need to change as long as agents keep returning the shared
schema (see schema.py).

Run directly for a demo of the full pipeline on mock data:
    python orchestrator.py
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from schema import SEVERITY_ORDER, validate_agent_output, SchemaError
from mock_agents import ALL_AGENTS


# ---------------------------------------------------------------------------
# Step 1: Trigger
# ---------------------------------------------------------------------------
def get_pr_diff() -> str:
    """Stand-in for pulling a real PR diff via GitHub API.

    Replace with an actual GitHub API call (or webhook payload parsing)
    once the Docs/Integration Dev's GitHub piece is ready. For now this
    just returns a placeholder string -- the mock agents ignore its
    content and return pre-seeded findings matching demo-repo/.
    """
    return "<mock PR diff — replace with real GitHub PR diff>"


# ---------------------------------------------------------------------------
# Step 2: Dispatch (parallel)
# ---------------------------------------------------------------------------
def dispatch_to_agents(pr_diff: str) -> list[dict]:
    """Run all subagents concurrently and return their raw outputs.

    Uses a thread pool to simulate calling Bob's subagents in parallel.
    When wired to real Bob 2.0 calls, this same structure lets you fire
    off multiple agent requests at once instead of sequentially.
    """
    results = []
    with ThreadPoolExecutor(max_workers=len(ALL_AGENTS)) as executor:
        futures = {executor.submit(agent, pr_diff): agent.__name__ for agent in ALL_AGENTS}
        for future in as_completed(futures):
            agent_name = futures[future]
            try:
                output = future.result()
                validate_agent_output(output)
                results.append(output)
            except SchemaError as e:
                # An agent that doesn't match the schema should be visible,
                # not silently dropped -- surface it as its own finding.
                print(f"[WARN] {agent_name} returned invalid output: {e}")
            except Exception as e:
                print(f"[ERROR] {agent_name} failed: {e}")
    return results


# ---------------------------------------------------------------------------
# Step 3 + 4: Collect and merge
# ---------------------------------------------------------------------------
def merge_reports(agent_outputs: list[dict]) -> dict:
    """Combine all subagent outputs into one prioritized report."""
    all_findings = []
    summaries = []

    for output in agent_outputs:
        all_findings.extend(output["findings"])
        summaries.append(f"[{output['agent']}] {output['summary']}")

    # De-duplicate findings that point at the same (file, line) --
    # keep the first one and append the extra message rather than
    # showing the same location twice.
    deduped = {}
    for f in all_findings:
        key = (f["file"], f["line"])
        if key in deduped:
            deduped[key]["message"] += f" | Also: {f['message']}"
        else:
            deduped[key] = dict(f)

    merged_findings = sorted(
        deduped.values(),
        key=lambda f: SEVERITY_ORDER.get(f["severity"], 99),
    )

    counts = {"blocking": 0, "warning": 0, "info": 0}
    for f in merged_findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1

    return {
        "counts": counts,
        "findings": merged_findings,
        "combined_summary": " ".join(summaries),
    }


# ---------------------------------------------------------------------------
# Step 5: Output
# ---------------------------------------------------------------------------
def format_report_as_markdown(report: dict) -> str:
    """Turn the merged report into a PR-comment-ready markdown string."""
    counts = report["counts"]
    lines = [
        "## PR Copilot Review",
        "",
        f"**{counts['blocking']} blocking** · {counts['warning']} warning · {counts['info']} info",
        "",
        report["combined_summary"],
        "",
        "| Severity | File | Line | Issue | Suggested fix |",
        "|---|---|---|---|---|",
    ]
    for f in report["findings"]:
        lines.append(
            f"| {f['severity']} | {f['file']} | {f['line']} | {f['message']} "
            f"| {f.get('suggested_fix', '')} |"
        )
    return "\n".join(lines)


def post_report(report_markdown: str) -> None:
    """Stand-in for posting the report as a PR comment via GitHub API.

    Replace with an actual `requests.post(...)` call to the GitHub Issues/
    PR comments API once the Docs/Integration Dev's GitHub piece is ready.
    """
    print(report_markdown)


# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------
def run_pipeline() -> None:
    pr_diff = get_pr_diff()
    agent_outputs = dispatch_to_agents(pr_diff)
    report = merge_reports(agent_outputs)
    report_markdown = format_report_as_markdown(report)
    post_report(report_markdown)


if __name__ == "__main__":
    run_pipeline()
