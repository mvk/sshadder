#!/usr/bin/env python
# pylint: disable=missing-docstring
from __future__ import print_function

import argparse
import sys

from . import sshadder


class CoolFormatter(argparse.RawTextHelpFormatter):
    def _get_help_string(self, action):
        _help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    _help += '\n[default: %(default)s]'
        return _help


def strlist(data):
    if not isinstance(data, str) or data is None:
        raise argparse.ArgumentTypeError(" ".join([
            "this parameter must be a string,"
            "optionally delimited with ','",
        ]))
    return data.split(',')


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="Bulk Loader of SSH private keys",
        formatter_class=CoolFormatter
    )
    parser.add_argument(
        '--init', '-i',
        action='store_true',
        dest='init',
        help='Create configuration file',
    )
    parser.add_argument(
        '--conf', '-c',
        dest='conf_file',
        help='Specify sshadder config yaml file',
        default=sshadder.DEFAULT_CONFS,
    )
    parser.add_argument(
        '--dotssh', '-s',
        dest='ssh_home',
        help='Alternative location for the private keys',
        default=sshadder.DEFAULT_SSH_HOME,
    )
    parser.add_argument(
        '--keys', '-k',
        dest='keys',
        help="Comma separated list of private keys to load in bulk",
        default=[sshadder.DEFAULT_SSH_KEY],
        type=strlist
    )
    parser.add_argument(
        '--version', '-v',
        dest='version',
        action='store_true',
        help='Print current version and exit'
    )
    if args is None:
        args = sys.argv[1:]

    result = parser.parse_args(args=args)
    return result


def main():
    cli_options = parse_args(args=sys.argv[1:])
    config = sshadder.get_config(cli_options=cli_options.__dict__)
    if cli_options.version:
        print("sshadder v{version}".format(version=sshadder.get_version()))
        return 0
    sshadder.ensure_ssh_agent()
    if cli_options.init:
        # initial setup flow:
        result = sshadder.gen_config(cli_options.__dict__)
        return result

    return sshadder.add_keys(
        config.get('keys'),
        decryptor=sshadder.simple_decryptor
    )


if __name__ == '__main__':
    sys.exit(main())
