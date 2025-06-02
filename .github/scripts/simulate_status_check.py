import os
import requests

# GitHub API and auth headers
GITHUB_API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
PR_NUMBER = os.getenv("PR_NUMBER")

if not all([TOKEN, REPO, PR_NUMBER]):
    raise Exception("Missing GITHUB_TOKEN, REPO, or PR_NUMBER environment variables")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_pr_commit_sha():
    url = f"{GITHUB_API}/repos/{REPO}/pulls/{PR_NUMBER}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["head"]["sha"]

def get_commit_status_by_sha_last_digit(sha):
    last_char = sha[-1].lower()
    return "success" if last_char in "02468ace" else "failure"

def set_commit_status(sha, state, description):
    url = f"{GITHUB_API}/repos/{REPO}/statuses/{sha}"
    data = {
        "state": state,
        "description": description,
        "context": "Simulated Commit Check"
    }
    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    print(f"✅ Set status to '{state}' for SHA {sha}")

def main():
    sha = get_pr_commit_sha()
    print(f"🔍 Last commit SHA: {sha}")

    status = get_commit_status_by_sha_last_digit(sha)
    description = "Simulated check passed." if status == "success" else "Simulated check failed."

    set_commit_status(sha, status, description)

if __name__ == "__main__":
    main()
