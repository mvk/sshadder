import sshadder
import argparse


def test_strlist():
    input_item = None
    try:
        sshadder.strlist(input_item)
        assert False, "unexpected no error"
    except argparse.ArgumentTypeError:
        assert True
    else:
        assert False, "unexpected error type"

    input_item = ["s"]
    try:
        sshadder.strlist(input_item)
        assert False, "unexpected no error"
    except argparse.ArgumentTypeError:
        assert True
    else:
        assert False, "unexpected error type"


    input_item = ""
    expected = [""]
    actual = sshadder.strlist(input_item)
    assert expected == actual

    input_item = "a,b"
    expected = ["a", "b"]
    actual = sshadder.strlist(input_item)
    assert expected == actual




#  TODO: add testing of return codes
def test_return_codes():
    pass
