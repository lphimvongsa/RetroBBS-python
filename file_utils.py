

import os
import pathlib


DISK_PATH = pathlib.Path("disk")

def _is_safe_path(file_path: os.DirEntry[str] | str | pathlib.Path):
    try:
        working_path = pathlib.Path(os.getcwd())/DISK_PATH
        _file_path = pathlib.Path(file_path)
        _abs_file_path = _file_path.resolve()
        return _abs_file_path.is_relative_to(working_path)
    except:
        return False


def file_exists(file_path: os.DirEntry[str] | str | pathlib.Path) -> bool:
    '''
    Returns true if a file exists at the specified path

    Throws an error if the file is outside the disk directory (since no files
    should be created outside of this directory for this assignment)

    Parameters:
    file_path (str): The path to the file
    '''
    if _is_safe_path(file_path):
        return os.path.exists(file_path)
    else:
        raise FileNotFoundError(f"Error: BBS should not use file paths outside of the disk directory ({DISK_PATH}), path was: {file_path}")
    

def remove_file(file_path: os.DirEntry[str] | str | pathlib.Path):
    '''
    Removes a file from the disk directory.
    Raises an error if the file is not within the DISK_PATH directory.

    Parameters:
    file_path (str): The path to the file to be removed
    '''
    if _is_safe_path(file_path):
        os.remove(file_path)
    else:
        raise FileNotFoundError(f"Files cannot be removed outside of disk directory: Path was: {file_path}, Directory is {DISK_PATH}")
    
def rename_file(old_path: os.DirEntry[str] | str | pathlib.Path, new_path: os.DirEntry[str] | str | pathlib.Path):
    '''
    Renames a file in the disk directory.
    Raises an error if the file is not within the DISK_PATH directory.

    Parameters:
    old_path (str): The path to the file to be renamed
    new_path (str): The new path for the file
    '''
    if _is_safe_path(old_path) and _is_safe_path(new_path):
        os.replace(old_path, new_path)
    else:
        raise FileNotFoundError(f"Files cannot be replaced outside of disk directory:  Old path was: {old_path}, New path was: {new_path}")
  

def clean_disk_directory():
    path = pathlib.Path(DISK_PATH)
    for f in path.glob("*"):
        if f.stem == ".keep": # Leave this blank file, which keeps git from deleting the directory
            continue
        remove_file(f)
