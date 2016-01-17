.. image:: https://travis-ci.org/mvk/sshadder.svg?branch=master
    :target: https://travis-ci.org/mvk/sshadder
=====    
About
=====
::
    During CLI work I often am using multiple password protected ssh keys.
    Multiple keys.  
    Then I need to load them, and it takes a minute or two.

    This project aims to save that time.


Usage
======

First time:
-----------
::
        sshadder -i

The text will guide you to give a master password (not saved anywhere), and then iterate over
 * key path
 * key password

When you're ready, choose 's' option to save and quit.
Each password is encrypted, then `base64.b64encode()`-ed and added to the key json item.


Next times:
-----------
::
        sshadder

Please refer to help, it shows default locations it's looking for the yaml files.

What it does not
~~~~~~~~~~~~~~~~
::
    SSH Agent management, You are responsible to run it,
    and have SSH_AUTH_SOCK properly pointing to the desired SSH Agent.

What it does
~~~~~~~~~~~~

Given config file `.sshagent.yml` and master password,
the utility adds all the ssh key files using their passwords
YAML file keeps the key passwords encrypted using simple-crypt package,
I am not sure how REALLY safe it is, but it is safer than plain text shell scripts.


Current known security problems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    I am using pexpect.spawn(), not sure how safe it is. If this is VERY unsafe for you,
    please send a patch/pull request :)


Contributing
============
Patches/pull requests are welcome to improve the code/fix bugs.
I don't want to integrate this with anything like lastpass, no external services.
Keepass integration would be nice though, given it's local (it could be non-local nowadays)




