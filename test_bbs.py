import importlib
import pytest


import bbs
import file_utils
from file_utils import DISK_PATH


def setup_function(request):
    global bbs
    bbs = importlib.reload(bbs) # Reload the BBS module, resetting any globals
    bbs.clean_reset()


def test_example():
    assert 2 == 1 + 1


def test_sample_From_handout():
    bbs.connect("kathi")
    msg_id = bbs.post_msg("post homework?", "is the handout ready?")
    bbs.post_msg("vscode headache", "reinstall to fix the config error")

    s1 = bbs.print_summary("headache")
    assert "Poster: kathi" in s1

    bbs.switch_user("nick")
    bbs.find_print_msg(msg_id)
    # assert ???  (What might we test about this message?)

    bbs.post_msg("handout followup", "yep, ready to go")
    bbs.remove_msg(msg_id)
    s2 = bbs.print_summary("followup")
    # assert ???  (What might we test at this point?)

"""for most of my tests i set the max messages to 4 so i could test the functionality
of the system at the cap. I also set the max messages to 4 in the bbs.py file."""

def test_connect():
    bbs.connect("kathi")
    bbs.post_msg("message 1", "reinstall to fix the config error")

    s1 = bbs.print_summary("message 1")
    assert "Poster: kathi" in s1

    bbs.disconnect()
    assert bbs.current_user == ""

    bbs.switch_user("nick")
    bbs.post_msg("message 2", "reinstall to fix the config error")
    s2 = bbs.print_summary("message 2")
    assert "Poster: nick" in s2

def test_disconnect():
    bbs.connect("kathi")
    assert bbs.current_user == "kathi"

    bbs.disconnect()
    assert bbs.current_user == ""

def test_post_msg():
    bbs.connect("kathi")
    msg_id = bbs.post_msg("message 1", "reinstall to fix the config error")
    assert msg_id == 1

    bbs.post_msg("message 2", "reinstall to fix the config error")
    s1 = bbs.print_summary("message 2")
    assert "Poster: kathi" in s1
    assert "Subject: message 2" in s1
    bbs.post_msg("message 3", "reinstall to fix the config error")
    bbs.post_msg("message 4", "reinstall to fix the config error")
    bbs.remove_msg(1)
    new_msg_id = bbs.post_msg("message 5", "reinstall to fix the config error")
    assert new_msg_id == 1

def test_remove_msg():
    bbs.connect("kathi")
    msg_id = bbs.post_msg("message 1", "reinstall to fix the config error")
    bbs.remove_msg(msg_id)

    s1 = bbs.print_summary("message 1")
    assert "Poster: kathi" not in s1

def test_print_summary():
    bbs.connect("kathi")
    bbs.post_msg("message 1", "reinstall to fix the config error")
    bbs.disconnect()
    bbs.connect("nick")
    bbs.post_msg("message 2", "reinstall to fix the config error")

    s1 = bbs.print_summary("message 1")
    assert "Poster: kathi" in s1
    assert "Subject: message 1" in s1

    s2 = bbs.print_summary("message 2")
    assert "Poster: nick" in s2
    assert "Subject: message 2" in s2

    s3 = bbs.print_summary("")
    assert "Poster: kathi" in s3
    assert "Poster: nick" in s3
    bbs.post_msg("message 2", "new message")
    s4 = bbs.print_summary("message 2")
    assert "Poster: nick" in s4
    assert "Subject: message 2" in s4
    assert "ID: 3" in s4
    assert "ID: 2" in s4

def test_summary_with_remove():
    bbs.connect("kathi")
    msg_id = bbs.post_msg("message 1", "reinstall to fix the config error")
    bbs.disconnect()
    bbs.switch_user("nick")
    bbs.post_msg("message 2", "reinstall to fix the config error")
    bbs.post_msg("message 3", "reinstall to fix the config error")
    bbs.post_msg("message 4", "reinstall to fix the config error")
    bbs.remove_msg(msg_id)

    s1 = bbs.print_summary("")
    assert "Poster: kathi" not in s1
    assert "Poster: nick" in s1
    assert "Subject: message 2" in s1
    assert "Subject: message 3" in s1
    assert "Subject: message 4" in s1
    s2 = bbs.print_summary("message 1")
    assert s2 == ""

def test_find_print_msg():
    bbs.connect("kathi")
    msg_id = bbs.post_msg("message 1", "reinstall to fix the config error") 
    bbs.disconnect()
    bbs.switch_user("nick")
    bbs.post_msg("message 2", "reinstall to fix the config error")
    bbs.post_msg("message 3", "reinstall to fix the config error")
    bbs.post_msg("message 4", "reinstall to fix the config error")

    s1 = bbs.find_print_msg(msg_id)
    assert "Poster: kathi" in s1

    s2 = bbs.find_print_msg(2)
    assert "Poster: nick" in s2

    bbs.remove_msg(msg_id)
    s3 = bbs.find_print_msg(msg_id)
    assert s3 == ""

    #check functionality at cap, next message will be 1 because it is only one in the list
    new_msg_id = bbs.post_msg("message 5", "reinstall to fix the config error")
    s4 = bbs.find_print_msg(new_msg_id)
    assert "Poster: nick" in s4
    assert "Subject: message 5" in s4
    assert new_msg_id == 1

    









    
    


