"""
Real GitHub API integration for orchestrator.py.

Copy the two functions below into orchestrator.py, replacing the existing
placeholder versions of get_pr_diff() and post_report(). Also copy the
three constants (GITHUB_API_BASE, GITHUB_TOKEN, REPO_OWNER, REPO_NAME) to
the top of the file, near DISPATCH_TIMEOUT_SECONDS.

Requires: pip install requests --break-system-packages
Requires: GITHUB_TOKEN environment variable set (see setup steps).
"""

import os
import requests

GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = "kidddzzz"      # change if your GitHub username differs
REPO_NAME = "PR-Copilot"     # change if you renamed the repo


# ---------------------------------------------------------------------------
# Step 1: Trigger (REAL VERSION)
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
# Step 5: Output (REAL VERSION)
# ---------------------------------------------------------------------------
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
# Also update run_pipeline() in orchestrator.py to look like this:
# ---------------------------------------------------------------------------
"""
def run_pipeline(pr_number: int) -> None:
    pr_diff = get_pr_diff(pr_number)
    agent_outputs = dispatch_to_agents(pr_diff)
    report = merge_reports(agent_outputs)
    report_markdown = format_report_as_markdown(report)
    post_report(pr_number, report_markdown)


if __name__ == "__main__":
    TEST_PR_NUMBER = 1  # <-- change this to your real test PR's number
    run_pipeline(TEST_PR_NUMBER)
"""
