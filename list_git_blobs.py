from git import Repo
from collections import defaultdict
import os
import json

def get_git_blobs(repo_path=None, verbose=False):
    """
    Generate a dictionary containing detailed information about a cloned Git repository.

    This function extracts various details from the specified Git repository, including
    the repository name, base path, remote URL, branch details, count of blobs (files),
    statistics of file types, and a list of blobs with their respective sizes.

    Args:
        repo_path (str): The file system path to the cloned Git repository.
        verbose (boolean): prints the output.

    Returns:
        dict: A dictionary with the following keys:
            - 'repo_name' (str): The name of the repository.
            - 'repo_base_path' (str): The base path of the repository.
            - 'repo_remote_url' (str or None): The URL of the remote repository, or None if not available.
            - 'repo_branch_details' (list of str): A list of branch names in the repository.
            - 'repo_blobs_count' (int): The total number of blobs (files) in the repository.
            - 'repo_type_stats' (dict): A dictionary with file extensions as keys and their counts as values.
            - 'repo_blobs' (list of dict): A list of dictionaries, each containing:
                - 'name' (str): The file path relative to the repository base.
                - 'size' (int): The size of the file in bytes.

    Raises:
        git.exc.InvalidGitRepositoryError: If the provided path is not a valid Git repository.
        git.exc.NoSuchPathError: If the provided path does not exist.
    """
    
    # Replace '/path/to/repo' with the path to your cloned repository
    repo_path = '/home/bhagavan/my-git-repos/genai'
    repo = Repo(repo_path)

    # Ensure the repository is not bare
    if repo.bare:
        return None

    # Retrieve repository name
    repo_name = os.path.basename(repo.working_tree_dir)

    # Retrieve repository base path
    repo_base_path = repo.working_tree_dir

    # Retrieve remote URL
    try:
        repo_remote_url = next(repo.remote().urls)
    except ValueError:
        repo_remote_url = None  # No remote found
        return None

    # Retrieve branch details
    repo_branch_details = [branch.name for branch in repo.branches]

    # Initialize counters
    repo_blobs_count = 0
    repo_type_stats = defaultdict(int)
    blobs_details = []

    # Traverse the repository tree to gather blob information
    for item in repo.head.commit.tree.traverse():
        if item.type == 'blob':  # 'blob' indicates a file
            repo_blobs_count += 1
            file_extension = os.path.splitext(item.path)[1].lstrip('.').lower()
            repo_type_stats[file_extension] += 1
            blobs_details.append({"name": item.path, "size": item.size})

    # Convert defaultdict to regular dict
    repo_type_stats = dict(repo_type_stats)

    # Compile the dictionary
    repo_details = {
        "repo_name": repo_name,
        "repo_base_path": repo_base_path,
        "repo_remote_url": repo_remote_url,
        "repo_branch_details": repo_branch_details,
        "repo_blobs_count": repo_blobs_count,
        "repo_type_stats": repo_type_stats,
        "blobs_details": blobs_details,
    }

    if verbose:
        print(json.dumps(repo_details, indent=4))
        
    return repo_details

def get_repo_details():
    repo_path = '/home/bhagavan/my-git-repos/genai'
    repo_details = get_git_blobs(repo_path, verbose=True)

    print(repo_details)

if __name__ == "__main__":
    get_repo_details()
