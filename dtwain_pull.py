# name: dtwain_pull
# author: joshua dwight
# github/jadwight

# this module helps grab the latest Dynarithmic TWAIN Library (DTWAIN) and packages it into a dtwain_core folder that can easily be interfaced with in python.

# pre-requisites: must have git installed or this module will not work!

# imports
import git
import os
import shutil
import zipfile
import time
import subprocess

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

def search_and_extract_file(search_file, search_path):
    pass

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

def search_and_extract_file(search_file, search_path):
    # Iterate through the directory and its subdirectories
    for root, _, files in os.walk(search_path):
        for file_name in files:
            if file_name == search_file:
                # Construct the full path to the zip file
                zip_file_path = os.path.join(root, file_name)

                # Extract the zip file into a directory with the same name
                extract_directory = os.path.splitext(zip_file_path)[0]  # Remove the .zip extension
                extract_directory = os.path.join(root, extract_directory)

                # Create the extraction directory if it doesn't exist
                os.makedirs(extract_directory, exist_ok=True)

                # Extract the zip file
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_directory)

                print(f"Extracted {search_file} from {zip_file_path} to {extract_directory}")

def extract_files():
    search_and_extract_file("release_libraries.zip", "./twain_library")

def ensure_dtwain_core_directory():
    # Get the current directory where the script is located
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Specify the names of the directories you want to create
    available_binaries = [
        "dtwain_x86",
        "dtwain_x86_unicode",
        "dtwain_x64",
        "dtwain_x64_unicode",
    ]

    for binaries in available_binaries:
        if not os.path.exists(os.path.join(current_directory, binaries)):
                              os.makedirs(os.path.join(current_directory, binaries))
                              print(f"`Created " + binaries)

def remove_directory(directory_path):
    try:
        # Wait for a short time to allow any ongoing operations to finish
        time.sleep(2)  # You can adjust the sleep time as needed

        # Use the os.system command to forcefully remove the directory
        cmd = f'rd /s /q "{directory_path}"'
        os.system(cmd)

        print(f"Successfully removed directory: {directory_path}")
    except Exception as e:
        print(f"Error removing directory with os.system: {str(e)}")

dtwain_x64_files = [
    "dtwain.py",
    "dtwain64.dll",
    "dtwain64.lib",
    "dtwain64.pdb",
    "dtwain64.ini",
    "twaininfo.txt",
    "twainlanguage.txt",
    "twainresourcestrings_english.txt"
]
dtwain_x64_unicode_files = [
    "dtwain.py",
    "dtwain64u.dll",
    "dtwain64u.lib",
    "dtwain64u.pdb",
    "dtwain64.ini",
    "twaininfo.txt",
    "twainlanguage.txt",
    "twainresourcestrings_english.txt"
]
dtwain_x86_files = [
    "dtwain.py",
    "dtwain32.dll",
    "dtwain32.lib",
    "dtwain32.pdb",
    "dtwain32_embarcadero.lib",
    "dtwain32.ini",
    "twaininfo.txt",
    "twainlanguage.txt",
    "twainresourcestrings_english.txt"
]
dtwain_x86_unicode_files = [
    "dtwain.py",
    "dtwain32u.dll",
    "dtwain32u.lib",
    "dtwain32u.pdb",
    "dtwain32u_embarcadero.lib",
    "dtwain32.ini",
    "twaininfo.txt",
    "twainlanguage.txt",
    "twainresourcestrings_english.txt"
]

pull_repo()
extract_files()
ensure_dtwain_core_directory()

search_dir = "./twain_library"

for file in dtwain_x64_files:
     search_and_copy_file(file, search_dir, "dtwain_x64")


for file in dtwain_x64_unicode_files:
     search_and_copy_file(file, search_dir, "dtwain_x64_unicode")

for file in dtwain_x86_files:
     search_and_copy_file(file, search_dir, "dtwain_x86")


for file in dtwain_x86_unicode_files:
     search_and_copy_file(file, search_dir, "dtwain_x86_unicode")

remove_directory("twain_library")