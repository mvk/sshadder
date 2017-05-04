#!/usr/bin/env python

from sshadder import cli


def test_strlist():
    input_item = None
    try:
        cli.strlist(input_item)
        assert False, "unexpected no error"
    except cli.argparse.ArgumentTypeError:
        assert True
    except:
        assert False, "unexpected error type"

    input_item = ["s"]
    try:
        cli.strlist(input_item)
        assert False, "unexpected no error"
    except cli.argparse.ArgumentTypeError:
        assert True
    except:
        assert False, "unexpected error type"

    input_item = ""
    expected = [""]
    actual = cli.strlist(input_item)
    assert expected == actual

    input_item = "a,b"
    expected = ["a", "b"]
    actual = cli.strlist(input_item)
    assert expected == actual


def test_parse_args():

    args = []
    expected_as_dict = dict(
        version=False,
        init=False,
        conf_file=cli.sshadder.DEFAULT_CONFS,
        ssh_home=cli.sshadder.DEFAULT_SSH_HOME,
        keys=[cli.sshadder.DEFAULT_SSH_KEY]
    )
    actual = cli.parse_args(args=args)
    for key, value in expected_as_dict.items():
        assert hasattr(actual, key)
        assert getattr(actual, key) == value

    args = ["-v"]
    expected_as_dict = dict(
        version=True,
        init=False,
        conf_file=cli.sshadder.DEFAULT_CONFS,
        ssh_home=cli.sshadder.DEFAULT_SSH_HOME,
        keys=[cli.sshadder.DEFAULT_SSH_KEY]
    )
    actual = cli.parse_args(args=args)
    for key, value in expected_as_dict.items():
        assert hasattr(actual, key)
        assert getattr(actual, key) == value

    args = ["-i"]
    expected_as_dict = dict(
        version=False,
        init=True,
        conf_file=cli.sshadder.DEFAULT_CONFS,
        ssh_home=cli.sshadder.DEFAULT_SSH_HOME,
        keys=[cli.sshadder.DEFAULT_SSH_KEY]
    )
    actual = cli.parse_args(args=args)
    for key, value in expected_as_dict.items():
        assert hasattr(actual, key)
        assert getattr(actual, key) == value

    expected_keys = [
        "/path/to/a",
        "/path/to/b",
    ]
    args = ["--keys=" + ','.join(expected_keys)]
    expected_as_dict = dict(
        version=False,
        init=False,
        conf_file=cli.sshadder.DEFAULT_CONFS,
        ssh_home=cli.sshadder.DEFAULT_SSH_HOME,
        keys=expected_keys
    )
    actual = cli.parse_args(args=args)
    for key, value in expected_as_dict.items():
        assert hasattr(actual, key)
        assert getattr(actual, key) == value

    expected_keys = [
        "/path/to/a",
        "/path/to/b",
    ]
    args = ["--keys=" + ','.join(expected_keys)]
    expected_as_dict = dict(
        version=False,
        init=False,
        conf_file=cli.sshadder.DEFAULT_CONFS,
        ssh_home=cli.sshadder.DEFAULT_SSH_HOME,
        keys=expected_keys
    )
    actual = cli.parse_args(args=args)
    for key, value in expected_as_dict.items():
        assert hasattr(actual, key)
        assert getattr(actual, key) == value
