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

import os
import requests

GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = "kidddzzz"      # change if your GitHub username differs
REPO_NAME = "PR-Copilot"     # change if you renamed the repo

# ---------------------------------------------------------------------------
# Step 1: Trigger
# ---------------------------------------------------------------------------
def get_pr_diff(pr_number: int) -> str:
    """Pull the real diff (changed files + patches) for a PR via GitHub API.
 
    Note: this now takes a pr_number argument, since it's a real PR instead
    of a mock placeholder. Update the call in run_pipeline() accordingly.
    """
    if not GITHUB_TOKEN:
        raise RuntimeError(
            "GITHUB_TOKEN environment variable is not set. "
            "See setup steps before running this."
        )
 
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # raises a clear error on 401/404/etc.
    files = response.json()
 
    if not files:
        return "(no changed files found in this PR)"
 
    diff_parts = []
    for f in files:
        filename = f["filename"]
        patch = f.get("patch", "(no text patch available for this file)")
        diff_parts.append(f"--- {filename} ---\n{patch}")
 
    return "\n\n".join(diff_parts)

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


def post_report(pr_number: int, report_markdown: str) -> None:
    """Post the merged review report as a real comment on the PR.
 
    Note: this now takes a pr_number argument too. GitHub treats PR
    comments as "issue comments" under the hood, so this uses the
    issues/comments endpoint even though it's a pull request.
    """
    if not GITHUB_TOKEN:
        raise RuntimeError(
            "GITHUB_TOKEN environment variable is not set. "
            "See setup steps before running this."
        )
 
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    response = requests.post(url, headers=headers, json={"body": report_markdown})
    response.raise_for_status()
 
    comment_url = response.json().get("html_url", "")
    print(f"Posted report to PR #{pr_number}: {comment_url}")


# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------
def run_pipeline(pr_number: int) -> None:
    pr_diff = get_pr_diff(pr_number)
    agent_outputs = dispatch_to_agents(pr_diff)
    report = merge_reports(agent_outputs)
    report_markdown = format_report_as_markdown(report)
    post_report(pr_number, report_markdown)
 
 
if __name__ == "__main__":
    TEST_PR_NUMBER = 1  # <-- change this to your real test PR's number
    run_pipeline(TEST_PR_NUMBER)
