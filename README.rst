.. image:: https://travis-ci.org/mvk/sshadder.svg?branch=master
    :target: https://travis-ci.org/mvk/sshadder

=====
About
=====


During CLI work I often am using multiple password protected ssh keys.

Multiple keys.  

Then I need to load them, and it takes a minute or two.

This project aims to save that time.


Usage
=====

First time:
-----------

Just run:::

    sshadder -i

The text will guide you to give a master password (not saved anywhere), and then iterate over

* key file path
* key password

When you're ready, choose 's' option to save and quit. Each password is encrypted and then ``base64.b64encode()``-ed and added to the key json item, so the text file is kept as it is now - text file.

Next times:
-----------

Run:::

    sshadder

Please refer to ``--help``, which shows default locations it's looking for the yaml files.

What it does not
~~~~~~~~~~~~~~~~

SSH Agent management. You are responsible to run it, and have ``SSH_AUTH_SOCK`` properly pointing to the desired SSH Agent.

What it does
~~~~~~~~~~~~

Given config file ``.sshagent.yml`` and master password, the utility adds all the ssh key files using their passwords ``YAML`` file keeps the key passwords encrypted using simple-crypt package.

Not sure how REALLY safe it is, but it is safer than plain text shell scripts.


Current known security problems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pexpect.spawn()`` is used here. Not sure how safe it is. If this is VERY unsafe for you, please send a patch/pull request :)


Contributing
============

Patches/pull requests are welcome to improve the code/fix bugs.

Let's try to avoid integrating with anything like lastpass, i.e. no external services in the meanwhile.

Keepass integration would be nice though, given it's local (it could be non-local nowadays)

If you have any other "better" ideas, please share, and I might be convinced.
