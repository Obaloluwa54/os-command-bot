import os
import subprocess
from core.config import REPOS_DIR, DATA_DIR

class GitHubManager:
    def __init__(self):
        if not os.path.exists(REPOS_DIR):
            os.makedirs(REPOS_DIR)

    def clone_repo(self, url):
        repo_name = url.strip("/").split("/")[-1].replace(".git","")
        dest = os.path.join(REPOS_DIR, repo_name)
        if os.path.exists(dest):
            return f"Repo {repo_name} already exists."
        try:
            subprocess.run(["git", "clone", url, dest], check=True)
            return f"Cloned {repo_name} successfully."
        except subprocess.CalledProcessError:
            return f"Failed to clone {repo_name}."

    def pull_repo(self, repo_name):
        path = os.path.join(REPOS_DIR, repo_name)
        if not os.path.exists(path):
            return f"Repo {repo_name} does not exist."
        try:
            subprocess.run(["git", "-C", path, "pull"], check=True)
            return f"Repo {repo_name} updated successfully."
        except subprocess.CalledProcessError:
            return f"Failed to update {repo_name}."

    def list_repos(self):
        return [d for d in os.listdir(REPOS_DIR) if os.path.isdir(os.path.join(REPOS_DIR, d))]
