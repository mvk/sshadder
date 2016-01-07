#!/usr/bin/env python
from __future__ import print_function
import argparse
import getpass
import json
import os
import pexpect
import sys

default_conf_file = 'sshadder.yaml'
user_home = os.environ.get('HOME', os.path.expanduser('~'))
default_ssh_home = os.path.join(user_home, '.ssh')
default_confs = [
    '.'.join(['', default_conf_file]),
    os.path.join(user_home, default_conf_file),
    os.path.join('/etc/sshadder', default_conf_file),
]


def get_config(cli_options=None):

    if not cli_options:
        return {}
    result = {}
    result.update(ssh_home=default_ssh_home)
    result.update(keys=[os.path.join(default_ssh_home, 'id_rsa')])
    conf_files = cli_options.get('conf_file')
    for conf_file in conf_files:
        if not os.path.exists(conf_file):
            continue
        if not os.path.isfile(conf_file):
            continue
        with open(conf_file, 'rb') as f:
            curr_conf_data = json.loads(f.read())
            ssh_home = curr_conf_data.get('ssh_home', result.get('ssh_home'))
            if 'keys' in curr_conf_data:
                curr_conf_data.update(keys=[os.path.join(ssh_home, key) for key in curr_conf_data.get('keys')])
            result.update(**curr_conf_data)
    return result


def strlist(data):
    try:
        int(data)
        raise argparse.ArgumentTypeError(" ".join([
            "this parameter must be a string,"
            "optionally delimited with ','",
        ]))
    except TypeError:
        pass
    return data.split(',')


class CoolFormatter(argparse.RawTextHelpFormatter):
    def _get_help_string(self, action):
        help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    help += '\n[default: %(default)s]'
        return help


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Bulk Loader of SSH private keys",
        formatter_class=CoolFormatter
    )
    parser.add_argument(
        '--conf', '-c',
        dest='conf_file',
        help='Specify sshadder config yaml file',
        default=default_confs,
    )
    parser.add_argument(
        '--dotssh', '-s',
        dest='ssh_home',
        help='Alternative location for the private keys',
        default=default_ssh_home,
    )
    parser.add_argument(
        '--keys', '-k',
        dest='keys',
        help="Comma separated list of private keys to load in bulk",
        default=[os.path.join(default_ssh_home, 'id_rsa')],
        type=strlist
    )
    result = parser.parse_args(args=args)
    return result


def ssh_add(key, password):
    print("Adding the key: {key} ... ".format(**locals()), end='')
    ssh_add_cmd = 'ssh-add {key}'
    ssh_adder = pexpect.spawn(ssh_add_cmd.format(**locals()))
    ssh_adder.expect('Enter passphrase for {key}:'.format(**locals()), timeout=0.5)
    ssh_adder.sendline(password)
    try:
        ssh_adder.expect(pexpect.EOF, timeout=0.5)
    except pexpect.ExceptionPexpect, pe:
        print("FAILED [exception data follows]")
        print("pexpect error: {pe}".format(**locals()), file=sys.stderr)
        return 1

    print("Done".format(**locals()))
    return ssh_adder.status


def add_keys(keys, password):
    for key_file in keys:
        result = ssh_add(key_file, password)
        assert 0 == result,\
            "Failed to add a key: {key_file}".format(**locals())
    return 0


def main():
    cli_options = parse_args(args=sys.argv[1:])
    config = get_config(cli_options=cli_options.__dict__)
    if not config.get('password'):
        password = getpass.getpass("Enter the password: ")
        config.update(password=password)
    return add_keys(config.get('keys'), config.get('password'))

if __name__ == '__main__':
    sys.exit(main())
