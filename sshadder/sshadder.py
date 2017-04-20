#!/usr/bin/env python
from __future__ import print_function
import argparse
import getpass
import json
import os
import pexpect
import sys
import base64
import simplecrypt

default_conf_file = 'sshadder.yaml'
user_home = os.environ.get('HOME', os.path.expanduser('~'))
default_ssh_home = os.path.join(user_home, '.ssh')
default_confs = [
    os.path.join(os.getcwd(), '.'.join(['', default_conf_file])),
    os.path.join(user_home, default_conf_file),
    os.path.join('/etc/sshadder', default_conf_file),
]


def getpass_double_prompt(description, max_attempts=3):
    result = None
    count = 0
    while not result:
        password1 = getpass.getpass(
            "Enter {description}: ".format(**locals())
        )
        password2 = getpass.getpass(
            "Repeat {description}: ".format(**locals())
        )
        if password1 != password2:
            count += 1
            msg_fmt = " ".join([
                "WARNING: passwords do not match,",
                "please repeat (attempt {0} out of {0})",
            ])
            print(msg_fmt.format(count, max_attempts))
            continue
        result = password1
    if not result:
        print("WARNING: Please re-run this application", file=sys.stderr)
        msg_fmt = "Failed to accept {description} more {max_attempts} times."
        raise argparse.ArgumentError(
            'password',
            message=msg_fmt.format(**locals())
        )
    return result


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
            keys = []
            if 'keys' in curr_conf_data:
                for item in curr_conf_data.get('keys'):
                    curr_key = item.get('path')
                    if not os.path.exists(curr_key):
                        item.update(path=os.path.join(ssh_home, curr_key))
                    keys.append(item)
            curr_conf_data.update(keys=keys)
        result.update(**curr_conf_data)
    return result


def gen_config(cli_options=None):
    if not cli_options:
        cli_options = dict(config_data=dict(keys=[]))
    config_data = cli_options.get("config_data", dict(keys=[]))
    prompt_fmt = "Enter config file path [default: {0}]: "
    config_fname = raw_input(prompt_fmt.format(default_confs[0]))
    if not config_fname:
        config_fname = cli_options.get("config_fname", default_confs[0])

    assert os.path.isdir(os.path.dirname(config_fname))
    keys_data = []
    master_password = getpass_double_prompt("Master Password")
    print(" ".join([
        "Master password accepted,",
        "it will be used to encrypt/decrypt the passwords",
    ]))
    print(" ".join([
        "WARNING: Please remember the Master password,",
        "otherwise the encrypted data will be useless",
    ]))
    enough = False
    save = False
    while not enough:
        key_path = raw_input("Enter private key file name: ")
        if not os.path.exists(key_path):
            print("WARNING: the file given does not exist")
            continue
        if not os.path.isfile(key_path):
            print("WARNING: the file given is not a file")
            continue
        print("The file given is accepted")
        key_password_plain = None
        try:
            key_password_plain = getpass_double_prompt(
                "Key {key_path} password".format(**locals()),
                max_attempts=1
            )
        except argparse.ArgumentError, ae:
            print("WARNING: Failed to accept key password.")
        if not key_password_plain:
            print("Automatically re-iterating")
            print("Please re-enter both key and its password")
            continue

        keys_data.append(dict(
            path=key_path,
            password=simple_encryptor(master_password, key_password_plain)
        ))

        print("Added the data on {key_path}".format(**locals()))
        prompt = " ".join([
            "Press",
            "'c' to continue,",
            "'s' to quit and save,",
            "or 'q' to quit and abort ",
        ])
        response = raw_input(prompt)
        if 'c' == response:
            continue
        elif 'q' == response:
            enough = True
            save = False
        elif 's' == response:
            enough = True
            save = True

    if not save:
        print("Not saving anything")
        return 0

    with open(config_fname, 'wb') as fd:
        fd.write(json.dumps(dict(keys=keys_data), indent=2))


def strlist(data):
    if not isinstance(data, str) or data is None:
        raise argparse.ArgumentTypeError(" ".join([
            "this parameter must be a string,"
            "optionally delimited with ','",
        ]))
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
        '--init', '-i',
        action='store_true',
        dest='init',
        help='Create configuration file',
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
    """
    Adds a keyfile protected by PLAIN TEXT password

    :param key: the private key file path
    :type key: str
    :param password: password of the key
    :type password: str

    """
    print("Adding the key: {key} ... ".format(**locals()), end='')
    ssh_add_cmd = 'ssh-add {key}'
    ssh_adder = pexpect.spawn(ssh_add_cmd.format(**locals()))
    ssh_adder.expect(
        'Enter passphrase for {key}:'.format(**locals()),
        timeout=0.5
    )
    ssh_adder.sendline(password)
    try:
        ssh_adder.expect(pexpect.EOF, timeout=0.5)
    except pexpect.ExceptionPexpect, pe:
        print("FAILED [exception data follows]")
        print("pexpect error: {pe}".format(**locals()), file=sys.stderr)
        return 1
    print("Done".format(**locals()))
    return 0


def simple_decryptor(password, ciphertext, enc='utf-8', unwrapper=None):
    """
    Decrypt ciphertext using password

    """
    if not unwrapper:
        unwrapper = base64.b64decode

    plaintext = simplecrypt.decrypt(
        password,
        unwrapper(ciphertext)
    ).decode(enc)
    return plaintext


def simple_encryptor(password, ciphertext, enc='utf-8', wrapper=None):
    """
    Decrypt ciphertext using password

    """
    if not wrapper:
        wrapper = base64.b64encode
    ciphertext = simplecrypt.encrypt(password, ciphertext)
    return wrapper(ciphertext)


def add_keys(keys, master_password, decryptor=None):

    if not decryptor:
        def decryptor(x, y):
            return x

    for key_item in keys:
        if not isinstance(key_item, dict):
            key_item = dict(path=key_item)

        key_file = key_item.get('path')
        key_password_hashed = key_item.get('password', master_password)

        result = ssh_add(
            key_file,
            decryptor(master_password, key_password_hashed)
        )
        assert 0 == result,\
            "Failed to add a key: {key_file}".format(**locals())
    return 0


def main():
    cli_options = parse_args(args=sys.argv[1:])
    config = get_config(cli_options=cli_options.__dict__)
    if cli_options.init:
        # initial setup flow:
        result = gen_config(cli_options.__dict__)
        return result

    master_password = getpass.getpass("Enter master password: ")
    return add_keys(
        config.get('keys'),
        master_password,
        decryptor=simple_decryptor
    )


if __name__ == '__main__':
    sys.exit(main())
