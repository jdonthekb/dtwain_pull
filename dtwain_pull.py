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
    
    # Specify the name of the directory you want to create
    dtwain_core_directory = os.path.join(current_directory, "dtwain_core")
    
    # Check if the directory already exists
    if not os.path.exists(dtwain_core_directory):
        # If it doesn't exist, create the directory
        os.makedirs(dtwain_core_directory)
        print(f"Created 'dtwain_core' directory at: {dtwain_core_directory}")
    else:
        print(f"'dtwain_core' directory already exists at: {dtwain_core_directory}")

def choose_dtwain_binary():
    available_binaries = [
        "dtwain_x86",
        "dtwain_x86_unicode",
        "dtwain_x64",
        "dtwain_x64_unicode",
    ]

    while True:
        print("Choose a dtwain binary:")
        for index, binary in enumerate(available_binaries, start=1):
            print(f"{index}. {binary}")
        
        try:
            choice = int(input("Enter the number (1-4): "))

            if 1 <= choice <= len(available_binaries):
                selected_binary = available_binaries[choice - 1]
                print(f"You chose: {selected_binary}")
                return selected_binary
            else:
                print("Invalid choice. Please enter a valid number (1-4).")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

""" # Example usage:
# Call choose_dtwain_binary() to let the user choose a dtwain binary.
chosen_binary = choose_dtwain_binary()

# Example of how to trigger a function based on the selected binary:
if chosen_binary == "dtwain_x86":
    print("Running function for dtwain_x86...")
    # Call the function for dtwain_x86
elif chosen_binary == "dtwain_x86_unicode":
    print("Running function for dtwain_x86_unicode...")
    # Call the function for dtwain_x86_unicode
elif chosen_binary == "dtwain_x64":
    print("Running function for dtwain_x64...")
    # Call the function for dtwain_x64
elif chosen_binary == "dtwain_x64_unicode":
    print("Running function for dtwain_x64_unicode...")
    # Call the function for dtwain_x64_unicode
 """


core_dir = "./dtwain_core"
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

# BINARIES
# path
repo_base = "./twain_library"
x86_binaries = os.path.join(repo_base, "32bit")
x64_binaries = os.path.join(repo_base, "64bit")

pull_repo()
extract_files()
ensure_dtwain_core_directory()

# Call choose_dtwain_binary() to let the user choose a dtwain binary.
chosen_binary = choose_dtwain_binary()
3
# trigger corresponding functions based on the selected binary:
if chosen_binary == "dtwain_x86":
    print("Running function for dtwain_x86...")
    # Call the function for dtwain_x86
    for file in dtwain_x86_files:
        copy_file_to_dtwain_core(file)
elif chosen_binary == "dtwain_x86_unicode":
    print("Running function for dtwain_x86_unicode...")
    # Call the function for dtwain_x86_unicode
    for file in dtwain_x86_unicode_files:
        copy_file_to_dtwain_core(file)
elif chosen_binary == "dtwain_x64":
    print("Running function for dtwain_x64...")
    # Call the function for dtwain_x64
    for file in dtwain_x64_files:
        copy_file_to_dtwain_core(file)
elif chosen_binary == "dtwain_x64_unicode":
    print("Running function for dtwain_x64_unicode...")
    # Call the function for dtwain_x64_unicode
    for file in dtwain_x64_unicode_files:
        copy_file_to_dtwain_core(file)
