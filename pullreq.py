import subprocess
import requests
import json
import os

# Load the GitHub token from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Ensure the token is not None
if GITHUB_TOKEN is None:
    raise ValueError("Please set the GITHUB_TOKEN environment variable")

# Replace these variables with your information
REPO_OWNER = 'muaddibusulll'  # Your GitHub username
FORKED_REPO_NAME = 'testlucifer1'  # Your fork's repository name
ORIGINAL_REPO_OWNER = 'tahaspc82442'  # Original repo owner
ORIGINAL_REPO_NAME = 'testlucifer1'  # Original repo name
HEAD_BRANCH = 'feature_changes'  # The branch with your changes
BASE_BRANCH = 'main'  # The branch you want to merge into
COMMIT_MESSAGE = 'Your commit message'
PR_TITLE = 'Add Feature X'
PR_BODY = 'This pull request adds feature X, which includes'

def run_git_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
        raise Exception(f"Git command failed: {command}")
    return result.stdout.strip()

try:
    # Stage changes
    print("Staging changes...")
    run_git_command('git add .')

    # Commit changes
    print("Committing changes...")
    run_git_command(f'git commit -m "{COMMIT_MESSAGE}"')

    # Push changes to your forked repository and set upstream
    print(f"Pushing changes to branch {HEAD_BRANCH} and setting upstream on your fork...")
    run_git_command(f'git push --set-upstream origin {HEAD_BRANCH}')

    # Create a pull request from your fork to the original repository
    print("Creating pull request...")
    url = f'https://api.github.com/repos/{ORIGINAL_REPO_OWNER}/{ORIGINAL_REPO_NAME}/pulls'

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    data = {
        'title': PR_TITLE,
        'head': f'{REPO_OWNER}:{HEAD_BRANCH}',
        'base': BASE_BRANCH,
        'body': PR_BODY
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print("Pull request created successfully!")
        pr_url = response.json().get('html_url')
        print(f"View it at: {pr_url}")
    else:
        print("Failed to create pull request")
        print(f"Response: {response.status_code}")
        print(response.json())
except Exception as e:
    print(f"An error occurred: {e}")
