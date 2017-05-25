#!/usr/bin/env python
# pylint: disable=missing-docstring
from __future__ import print_function

import argparse
import base64
import getpass
import json
import os
import stat
import sys
import pexpect
import pkg_resources
import simplecrypt

DEFAULT_CONF_FILE = 'sshadder.json'
USER_HOME = os.environ.get('HOME', os.path.expanduser('~'))
DEFAULT_SSH_HOME = os.path.join(USER_HOME, '.ssh')
DEFAULT_SSH_KEY = os.path.join(DEFAULT_SSH_HOME, 'id_rsa')
DEFAULT_CONFS = [
    os.path.join(os.getcwd(), '.'.join(['', DEFAULT_CONF_FILE])),
    os.path.join(USER_HOME, '.'.join(['', DEFAULT_CONF_FILE])),
    os.path.join('/etc/sshadder', DEFAULT_CONF_FILE),
]


def get_version():
    version = '0.0.0-unknown'
    try:
        version = pkg_resources.get_distribution('sshadder').version
    except pkg_resources.DistributionNotFound:
        pass
    return version


def getpass_double_prompt(description, max_attempts=3):
    result = None
    count = 0
    while not result:
        password1 = getpass.getpass(" ".join(["Enter", description + ":", ""]))
        password2 = getpass.getpass(" ".join(["Repeat", description + ":", ""]))
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


def short_help():
    print("\n".join([
        "Please ensure ssh-agent is running and:",
        "  - its environment variable SSH_AUTH_SOCK is properly set",
        "  - the environment variable is pointing to correct socket file",
        "",
    ]))


def ensure_ssh_agent():
    ssh_agent_sock = 'SSH_AUTH_SOCK'
    if ssh_agent_sock not in os.environ:
        print("FATAL: environment variable {ssh_agent_sock} is unset.".format(**locals()))
        short_help()
        sys.exit(1)
    if not os.path.exists(os.environ.get(ssh_agent_sock)):
        print("FATAL: environment variable {ssh_agent_sock} does not point to an existing file.".format(**locals()))
        short_help()
        sys.exit(1)

    sock_mode = os.stat(os.environ.get('SSH_AUTH_SOCK')).st_mode
    if not stat.S_ISSOCK(sock_mode):
        print("FATAL: environment variable {ssh_agent_sock} does not point to a socket.".format(**locals()))
        short_help()
        sys.exit(1)
    print("{ssh_agent_sock} variable is OK".format(**locals()))


def get_config(cli_options=None):
    if not cli_options:
        return {}
    result = {}
    result.update(dict(ssh_home=DEFAULT_SSH_HOME))
    result.update(dict(keys=[os.path.join(DEFAULT_SSH_HOME, 'id_rsa')]))
    conf_files = cli_options.get('conf_file')
    for conf_file in conf_files:
        if not os.path.exists(conf_file):
            continue
        if not os.path.isfile(conf_file):
            continue
        with open(conf_file, 'rb') as rfd:
            curr_conf_data = json.loads(rfd.read())
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
    # config_data = cli_options.get("config_data", dict(keys=[]))
    prompt_fmt = "Enter config file path [default: {0}]: "
    config_fname = input(prompt_fmt.format(DEFAULT_CONFS[0]))
    if not config_fname:
        config_fname = cli_options.get("config_fname", DEFAULT_CONFS[0])

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
        key_path = input("Enter private key file name: ")
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
        except argparse.ArgumentError:
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
        response = input(prompt)
        if response == 'c':
            continue
        elif response == 'q':
            enough = True
            save = False
        elif response == 's':
            enough = True
            save = True

    if not save:
        print("Not saving anything")
        return 0

    with open(config_fname, 'wb') as wfd:
        wfd.write(json.dumps(dict(keys=keys_data), indent=2))


def ssh_add(key, password=None):
    """
    Adds a keyfile protected by PLAIN TEXT password

    :param key: the private key file path
    :type key: str
    :param password: password of the key
    :type password: str

    """
    print("Adding: {key} ... ".format(key=key), end='')
    ssh_add_cmd = 'ssh-add {key}'
    ssh_adder = pexpect.spawn(ssh_add_cmd.format(**locals()))
    ssh_adder.expect(
        'Enter passphrase for {key}:'.format(**locals()),
        timeout=0.5
    )
    ssh_adder.sendline(password)
    try:
        ssh_adder.expect(pexpect.EOF, timeout=0.5)
    except pexpect.ExceptionPexpect as epe:
        print("FAILED [exception data follows]")
        print("pexpect error: {epe}".format(epe=epe), file=sys.stderr)
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


def simple_encryptor(password, ciphertext, enc=None, wrapper=None):
    """
    Decrypt ciphertext using password

    """
    if enc is None:
        enc = 'utf-8'
    if not wrapper:
        wrapper = base64.b64encode
    ciphertext = simplecrypt.encrypt(password.encode(enc), ciphertext.encode(enc))
    return wrapper(ciphertext)


def add_keys(keys, master_password=None, decryptor=None):
    if master_password is None:
        master_password = getpass.getpass("Enter master password: ")

    if not decryptor:
        # pylint: disable=unused-argument
        # noinspection PyUnusedLocal
        def _decryptor(password, password_hashed):
            return password
        decryptor = _decryptor

    for key_item in keys:
        if not isinstance(key_item, dict):
            key_item = dict(path=key_item)

        key_file = key_item.get('path')
        key_password_hashed = key_item.get('password', master_password)

        result = ssh_add(
            key_file,
            decryptor(master_password, key_password_hashed)
        )
        assert result == 0, \
            "Failed to add a key: {key_file}".format(**locals())
    return 0
