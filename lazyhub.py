import os
from git import Repo
import schedule
import time
from datetime import datetime

# Path to the local repository
REPO_PATH = "/path/to/your/repo"
GITHUB_REMOTE = "origin"  # Typically 'origin'

def generate_commit_message(repo):
    """Generate a commit message with changed files and statistics."""
    try:
        diff = repo.git.diff('--stat', '--cached').strip()  # Get change statistics
        changed_files = [item.a_path for item in repo.index.diff(None)]  # Changed files
        
        if not changed_files:
            return None  # No changes, no commit needed
        
        files_list = "\n".join(f"- {file}" for file in changed_files)
        commit_message = (
            f"LazyHub auto-commit on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Changed files:\n{files_list}\n\n"
            f"Git stats:\n{diff}"
        )
        return commit_message
    except Exception as e:
        print(f"Error generating commit message: {e}")
        return "Auto-commit without detailed stats"

def check_and_push_changes():
    try:
        # Load the repository
        repo = Repo(REPO_PATH)
        
        # Check for changes
        if repo.is_dirty(untracked_files=True):  # Check changes including untracked files
            print("Changes found. Preparing for commit.")
            
            # Add changes
            repo.git.add(all=True)
            
            # Generate commit message
            commit_message = generate_commit_message(repo)
            if not commit_message:
                print("No changes to commit.")
                return
            
            # Commit
            repo.index.commit(commit_message)
            print(f"Changes committed: {commit_message}")
            
            # Push changes to GitHub
            origin = repo.remote(name=GITHUB_REMOTE)
            origin.push()
            print("Changes successfully pushed to GitHub.")
        else:
            print("No changes found.")
    except Exception as e:
        print(f"Error: {e}")

# Schedule daily execution
schedule.every().day.at("00:00").do(check_and_push_changes)

print("Script started. Waiting...")
while True:
    schedule.run_pending()
    time.sleep(60)
