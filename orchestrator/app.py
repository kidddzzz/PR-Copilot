import os
from flask import Flask, request, jsonify
from orchestrator import run_pipeline

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "PR Copilot Webhook is active"}), 200

@app.route("/webhook", methods=["POST"])
def github_webhook():
    event = request.headers.get("X-GitHub-Event")
    payload = request.json or {}

    # Handle Pull Request events (opened or updated)
    if event == "pull_request" and payload.get("action") in ["opened", "synchronize", "reopened"]:
        pr_number = payload["pull_request"]["number"]
        print(f"Triggering PR Copilot pipeline for PR #{pr_number}")
        
        try:
            run_pipeline(pr_number)
            return jsonify({"status": "success", "pr_number": pr_number}), 200
        except Exception as e:
            print(f"Error executing pipeline: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "ignored", "reason": f"Event '{event}' action '{payload.get('action')}' not targeted"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)