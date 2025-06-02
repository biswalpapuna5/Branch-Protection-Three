import os
import requests
import sys

GITHUB_API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
PR_NUMBER = os.getenv("PR_NUMBER")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_pr_commit_sha():
    url = f"{GITHUB_API}/repos/{REPO}/pulls/{PR_NUMBER}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["head"]["sha"]

def is_sha_even(sha):
    last_char = sha[-1].lower()
    return last_char in "02468ace"

def post_commit_status(sha, state, description):
    url = f"{GITHUB_API}/repos/{REPO}/statuses/{sha}"
    data = {
        "state": state,
        "description": description,
        "context": "Simulated Commit Check"
    }
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code != 201:
        print(f"❌ Failed to set status: {resp.status_code} - {resp.text}")
        resp.raise_for_status()
    print(f"✅ Status '{state}' set on commit {sha}.")

def comment_on_pr(message):
    url = f"{GITHUB_API}/repos/{REPO}/issues/{PR_NUMBER}/comments"
    data = {"body": message}
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code != 201:
        print(f"❌ Failed to post comment: {resp.status_code} - {resp.text}")
        resp.raise_for_status()
    print("💬 Comment posted on PR.")

def main():
    sha = get_pr_commit_sha()
    print(f"🔍 Latest commit SHA: {sha}")

    if is_sha_even(sha):
        post_commit_status(sha, "success", "Simulated status check passed.")
        comment_on_pr("✅ Status check passed. You can now merge this pull request.")
    else:
        post_commit_status(sha, "failure", "Simulated status check failed.")
        comment_on_pr("❌ Status check failed. You cannot merge this pull request yet.")
        sys.exit(1)  # Fail the workflow to block merge

if __name__ == "__main__":
    main()
