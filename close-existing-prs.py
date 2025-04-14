import requests
import os

github_token = os.environ.get("GITHUB_TOKEN")
repo_owner = os.environ.get("REPO_OWNER")
repo_name = os.environ.get("REPO_NAME")
head_branch = os.environ.get("HEAD_BRANCH")

headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

# List open pull requests
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls?state=open&head={head_branch}"
response = requests.get(api_url, headers=headers)
response.raise_for_status()
open_prs = response.json()

print(f"Found {len(open_prs)} open PRs for branch '{head_branch}'.")

# Close each open pull request
for pr in open_prs:
    pr_number = pr["number"]
    close_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    payload = {"state": "closed"}
    close_response = requests.patch(close_url, headers=headers, json=payload)
    close_response.raise_for_status()
    print(f"Closed pull request #{pr_number}: {pr['title']}")