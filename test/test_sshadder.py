import argparse
import simplecrypt
import base64
from sshadder import sshadder


def test_simple_encryptor():
    password = 'myc00lp@ssw0rd'
    expected = str('myc00lerp@ssw0rd!').encode('utf-8')
    cipher = sshadder.simple_encryptor(password, expected.decode('utf-8'))
    actual = simplecrypt.decrypt(password, base64.b64decode(cipher))
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
