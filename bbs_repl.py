
import bbs

def show_menu(): 
    """
    Prints the menu of options.
    """
    print("Please select an option: ")
    print("  - type A <subj> <msg> to add a message")
    print("  - type D <msg-num> to delete a message")
    print("  - type S for a summary of all messages")
    print("  - type S <text> for a summary of messages with <text> in title or poster")
    print("  - type P <msg-num> to print the contents of a message")
    print("  - type X to exit")
    print("  - type U to switch user")
    print("  - type R to reset the BBS, deleting all posts!")
    print("  - type H to display this help")


def get_username():
    while True:
        input_str = input("Enter a username: ")
        tokens = input_str.split(" ")
        if len(tokens) != 1:
            print("Error:  Username must be one word")
            continue

        return tokens[0].strip()

def main():
    """
    Loop to run the system. It does not do error checking on the inputs that
    are entered (and you do not need to fix that problem)
    """
    
    prompt_str = "Enter a command ('H' for help) > "
    print("Welcome to our BBS!")
    username = get_username()
    bbs.connect(username)

    print(bbs.PRINT_SEP)
    print(f"Welcome {username}!")
    show_menu()
    print(bbs.PRINT_SEP)

    done = False
    while(not done):
        whole_input = input(prompt_str) # read the user command
        choice = bbs.split_string_exclude_quotes(whole_input) # split into quotes
        match choice[0].upper():
            case "A": 
                if len(choice) != 3:
                    print("Usage:  A <subj> <msg>")
                    print("(If <subj> or <msg> is more than one word, put them in \"double quotes\")")
                    continue
                try:
                    new_id = bbs.post_msg(choice[1], choice[2]) # subject, text
                    print(f"Created message {new_id}")
                except bbs.MessagesFullExn:
                    print("No more space for messages!")
            case "D": 
                if len(choice) != 2:
                    print("Usage: D <msg-num>")
                    continue
                bbs.remove_msg(int(choice[1]))
                print(f"Removed message {int(choice[1])}")
            case "S": 
                if len(choice) == 1:
                    bbs.print_summary("")
                else:
                    term = choice[1]
                    bbs.print_summary(term)
            case "P":
                if len(choice) != 2:
                    print("Usage: P <msg-num>")
                    continue
                bbs.find_print_msg(int(choice[1]))
            case "X": 
                bbs.disconnect()
                done = True
                exit()
            case "R":
                bbs.clean_reset()
                print("System reset!")
            case "U":
                # restart menu
                new_username = get_username()
                bbs.switch_user(new_username)
            case "H":
                show_menu()
            case _: 
                print("Unknown command")


# This runs the main function when bbs_repl.py 
# is run directly from the terminal 
if __name__ == "__main__":
    main()