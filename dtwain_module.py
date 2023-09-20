import git
import os
import shutil

class Progress(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(f"Progress: {self._cur_line}")

def pull_latest_from_repository(repo_url, local_path):
    """
    Pull the latest changes from a Git repository with verbose output.

    Parameters:
        repo_url (str): The URL of the Git repository to pull from.
        local_path (str): The local directory where the repository is cloned.

    Returns:
        str: A message indicating the pull status.
    """
    print(f"Checking if directory {local_path} exists...")
    
    # Check if the directory exists; create it if it doesn't
    if not os.path.exists(local_path):
        print(f"Directory {local_path} does not exist. Creating it...")
        os.makedirs(local_path)

    try:
        # Check if the repository already exists locally
        print(f"Checking if {local_path} is a Git repository...")
        repo = git.Repo(local_path)
    except git.InvalidGitRepositoryError:
        # Check if the directory is empty
        if not os.listdir(local_path):
            # If empty, clone the repository
            print(f"Directory {local_path} is empty. Cloning repository...")
            repo = git.Repo.clone_from(repo_url, local_path, progress=Progress())
        else:
            print(f"Directory {local_path} is not empty. Cleaning it out...")
            shutil.rmtree(local_path)
            os.makedirs(local_path)
            print(f"Cloning repository into clean directory {local_path}...")
            repo = git.Repo.clone_from(repo_url, local_path, progress=Progress())

    # Get the remote repository
    print("Fetching remote repository...")
    remote = repo.remote()

    # Pull the latest changes
    print("Pulling latest changes...")
    pull_info = remote.pull()

    # Check if the pull was successful
    if pull_info[0].flags > 0:
        return "Successfully pulled latest changes."
    else:
        return "Already up-to-date."

def pull_repo():   
    # Example usage
    repo_url = "https://github.com/dynarithmic/twain_library.git"
    local_path = "./twain_library"  # Replace with your desired local path

    result = pull_latest_from_repository(repo_url, local_path)
    print(result)

def search_and_copy_file(search_file, search_path, copy_to):
    """
    Search for a file in a directory and its subdirectories, then copy it to a new location.

    Parameters:
        search_file (str): The name of the file to search for.
        search_path (str): The directory path to start the search.
        copy_to (str): The directory path to copy the file to.

    Returns:
        str: A message indicating the search and copy status.
    """
    for root, dirs, files in os.walk(search_path):
        if search_file in files:
            file_path = os.path.join(root, search_file)
            print(f"Found {search_file} at {file_path}")

            # Check if the destination directory exists; create it if it doesn't
            if not os.path.exists(copy_to):
                print(f"Directory {copy_to} does not exist. Creating it...")
                os.makedirs(copy_to)

            # Copy the file
            shutil.copy(file_path, copy_to)
            return f"Successfully copied {search_file} to {copy_to}"

    return f"{search_file} not found in {search_path}"

def copy_file_to_dtwain_core(search_file):
    """
    Search for a file in the ./twain_library directory and its subdirectories,
    then copy it to the ./dtwain_core directory.

    Parameters:
        search_file (str): The name of the file to search for.

    Returns:
        str: A message indicating the search and copy status.
    """
    search_path = "./twain_library"
    copy_to = "./dtwain_core"
    return search_and_copy_file(search_file, search_path, copy_to)

def build_core():
    dtwain_x64_files = ""
    dtwain_x64_unicode_files = ""
    dtwain_x86_files = ""
    dtwain_x86_unicode_files = ""