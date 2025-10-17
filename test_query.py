
import pathlib
import pytest

import query_slow as qslow
import query_several as qs

WIKIS_DIR = pathlib.Path("wikis")
CS200_WIKI = WIKIS_DIR/"CS200Wiki.xml"

def test_example_slow():
    q = qslow.QuerySlow(CS200_WIKI)
    result = q.query("Collaboration")
    assert "CS200 Collaboration Details" in result


def test_example_single():
    q = qs.QuerySeveral(CS200_WIKI)
    result = q.query("Collaboration")
    assert "CS200 Collaboration Details" in result