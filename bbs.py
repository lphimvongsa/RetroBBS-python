

import os       # for file handling  
import sys      # for writing/printing messages
import math
import pathlib  # Helpers for working with paths

import re    # for splitting input

from file_utils import remove_file, rename_file, clean_disk_directory, file_exists

######### STENCIL CONSTANTS (DO NOT CHANGE) ######################
DISK_PATH = pathlib.Path("disk") # path to store files, relative to current directory
PRINT_SEP = "====" # used to separate messages when printing them out



######### GLOBAL VARIABLES ############################
current_user : str


######### EXCEPTIONS #################################################
class MessagesFullExn(Exception):
    pass


####### CORE API FUNCTIONS ####################################

def connect(username: str):
    """
    Starts a connection to the system by the named user.

    You may assume the username is well-formed (ie, within the character
    limits).

    Parameters:
    username -- the name of the user who is connecting (they will be the
                poster of messages added until they disconnect)
    """
    
    global current_user
    current_user = username

def disconnect():
    """
    Disconnects the current user and saves data as necessary so that the system
    can resume even if the Python program is restarted.
    
    What you do here will depend on your design:
     - You may want to wait to implement this until you implement post_msg
     - It's not wrong if this function does nothing (your design might do the
       same work in other functions)
    """
    global current_user
    current_user = ""
    

def switch_user(username: str):
    """
    Switch to a different user (without disconnecting)

    You may assume the username is well-formed (ie, within the character limits)
    """
    
    global current_user
    current_user = username


def clean_reset():
    """
    Deletes all the disk files to start a clean run of the system.  
    THIS FUNCTION WILL BE RUN BEFORE EACH TEST.  Use it to reset globals,
    constants, etc. back to a starting state when the BBS is empty.

    We've started this function for you:  clean_disk_directory() removes any
    files in DISK_PATH.  In addition, you should add to this function to reset
    any globals you use back to their starting state.
    """
    clean_disk_directory() # DO NOT REMOVE THIS
    global current_user
    # create 19 message files
    for i in range(19): 
        file_path = DISK_PATH / f"messages_{i}.txt"
        with open(file_path, "w") as f:
            pass
    
    file_path = DISK_PATH / f"available_ids.txt"
    # create available_ids.txt file with each id on a new line
    with open(file_path, "w") as f:
        for k in range(1, 201):
            f.write(str(k) + "\n")
    

    
    current_user = ""


def post_msg(subj: str, msg: str) -> int:
    """
    Stores a new message (however it makes sense for your design). Your code
    should determine what ID to use for the message, and the poster of the
    message should be the user who is connected when this function is called.

    You can assume that both the subj and msg fields are within
    the character limits.

    Parameters:
    subj -- subject line
    msg -- message body

    Returns:  the ID number of the message created (for autograder)
    """
    # Get the next available message ID from available_ids.txt
    message_id = get_id()

    # determine which file to store the message
    file_index = (int(message_id) - 1) // 11 
    file_path = DISK_PATH / f"messages_{file_index}.txt"
    
    # write the message into the file at the first available empty line
    with open(file_path, "a") as f_append:
        f_append.write(f"{message_id}\n{current_user}\n{subj}\n{msg}\n")
        
    return int(message_id)



def find_print_msg(id: int) -> str:
    """
    Prints contents of message for given ID. 

    Parameters:
    id -- message ID

    Returns:
    The string to be printed (for autograder).  If the message is not found,
    returns an empty string.
    """
    # determine which file the message is in
    file_index = (id - 1)// 11  
    file_path = DISK_PATH / f"messages_{file_index}.txt"
    with open(file_path, "r+") as f:
        while True:
            line = f.readline()
            
            if line == "": #reached end of file
                return "" 
            if line.strip() == str(id):
                # return next 4 lines
                user = f.readline().strip()
                subj = f.readline().strip()
                msg = f.readline().strip()
                return print_msg(id, user, subj, msg)
    
            


def remove_msg(id: int):
    """
    Removes a message from however your design is storing it. A removed message
    should no longer appear in summaries, be available to print, etc.

    You may assume the message exists.
    """
    file_index = (id - 1) // 11
    file_path = DISK_PATH / f"messages_{file_index}.txt"
    updated_content = ""

    with open(file_path, "r+") as f:
        while True:
            id_line = f.readline()
            if id_line == "":
                break  # reached end of file

            user_line = f.readline()
            subj_line = f.readline()
            body_line = f.readline()

            if id_line.strip() == str(id):
                # skip message to remove
                continue
            else:
                updated_content += id_line
                updated_content += user_line
                updated_content += subj_line
                updated_content += body_line

    with open(file_path, "w") as f:
        f.write(updated_content)

    # add ID back to available_ids
    available_ids_path = DISK_PATH / "available_ids.txt"
    with open(available_ids_path, "a") as f:
        f.write(f"{id}\n")


def print_summary(term) -> str:
    """
    Prints summary of messages that have the search term in the user or subj fields.
    A search string of "" will match all messages.
    Summary does not need to present messages in order of IDs.

    Returns:
    A string to be printed with the summary text (for autograder)
    If there are no messages, return an empty string.
    """
    
    summary = ""
    for file_index in range(19):
        file_path = DISK_PATH / f"messages_{file_index}.txt"
        with open(file_path, "r") as f:
            while True:
                id_line = f.readline()
                if id_line == "":
                    break  # break out of loop once reach end of file
                
                # get the user, subject, and body 
                user_line = f.readline().strip()
                subj_line = f.readline().strip()
                body_line = f.readline().strip()

                # Check if search term is in user or subject
                if term in user_line or term in subj_line or term == "":
                    summary += print_msg(int(id_line.strip()), user_line, subj_line, None) + "\n"

    return summary






######## HELPERS ##########################################

def format_print_msg(id: int, user: str, subj: str, msg: str=None, do_print=False) -> str:
    """
    Create a string representing a message in the correct format to print
    to the terminal:
       - if msg=None, only summary is printed.
       - if do_print=True, prints the message to a terminal as well


    Parameters:
    id -- message id
    user -- poster
    subj -- subject line
    msg -- body text (optional, only summary printed if set to None)
    do_print - if true, print the message to the string as well

    Returns:
    string of the message in correct format (for autograder)
    """
    output_str = ""
    output_str += PRINT_SEP
    output_str += f"\nID: {id}"
    output_str += f"\nPoster: {user}"
    output_str += f"\nSubject: {subj}\n"

    if msg is not None:
        output_str += f"Message: {msg}\n"

    output_str += PRINT_SEP

    if do_print:
        print(output_str)

    return output_str

def print_msg(id: int, user: str, subj: str, msg: str=None) -> str:
    """
    Print a message to the terminal in the correct format
    (This is just a shortcut for calling format_msg with do_print=True)

    Parameters:
    id -- message id
    user -- poster
    subj -- subject line
    msg -- body text (optional, use msg=None to only print summary)
        
    Returns:
    string of the message in correct format (for autograder)
    """
    return format_print_msg(id, user, subj, msg, do_print=True)

def split_string_exclude_quotes(s) -> list[str]:
    """
    Splits a given string and splits it based on spaces, while also grouping
    words in double quotes together.

    Parameters:
    s -- string to be split
    Returns:
    A list of strings after splitting
    Example:
    'separate "these are together" separate` --> ["separate", "these are together", "separate"]
    """
    # This pattern matches a word outside quotes or captures a sequence of
    # characters inside double quotes without including the quotes
    pattern = r'"([^"]*)"|(\S+)'
    matches = re.findall(pattern, s)
    # Each match is a tuple, so we join non-empty elements
    return [m[0] if m[0] else m[1] for m in matches]

def get_id() -> str:
    """
    helper method that getst the next available id from the available_ids.txt file
    and removes it from the file.  If no ids are available, raises an exception.
    
    returns the id as a string"""

    src_path = DISK_PATH / "available_ids.txt"
    id_found = ""
    remaining_content = ""

    with open(src_path, "r") as f:
        while True:
            line = f.readline()
            if line == "":
                break
            if id_found == "" and line.strip() != "":
                id_found = line.strip()
                continue  # remove this line
            remaining_content += line  # keep all other lines

    if id_found == "":
        raise MessagesFullExn("No available IDs.")

    with open(src_path, "w") as f:
        f.write(remaining_content)

    return id_found
                

