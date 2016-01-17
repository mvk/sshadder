import argparse
import sshadder.sshadder as sshadder
import simplecrypt
import base64


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


def test_simple_encryptor():
    password = 'myc00lp@ssw0rd'
    expected = 'myc00lerp@ssw0rd!'
    cipher = sshadder.simple_encryptor(password, expected)
    actual = simplecrypt.decrypt(password, base64.b64decode(cipher)).encode('utf-8')
    assert expected == actual


def test_simple_decryptor():
    password = 'myc00lp@ssw0rd'
    expected = 'myc00lerp@ssw0rd!'
    cipher = base64.b64encode(simplecrypt.encrypt(password, expected))
    actual = sshadder.simple_decryptor(password, cipher)
    assert expected == actual


#  TODO: add testing of return codes
def test_return_codes():
    pass
