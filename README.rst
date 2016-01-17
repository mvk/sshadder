About
=====

.. image:: https://travis-ci.org/mvk/sshadder.svg?branch=master
    :target: https://travis-ci.org/mvk/sshadder


During CLI work I often am using multiple password protected ssh keys.
Multiple keys.  
Then I need to load them, and it takes a minute or two.

This project aims to save that time.

Usage
======

First time:
-----------

        sshadder -i


Next times:
-----------

        sshadder


What it does not
~~~~~~~~~~~~~~~~

SSH Agent management, You are responsible to run it  
and have SSH_AUTH_SOCK properly pointing to the desired SSH Agent.

What it does
~~~~~~~~~~~~

Given config file `.sshagent.yml` and master password,
the utility adds all the ssh key files using their passwords
YAML file keeps the key passwords encrypted using simple-crypt package,
I am not sure how REALLY safe it is, but it is safer than plain text shell scripts.


Contributing
============
Patches are welcome to improve the code/fix bugs.
I don't want to integrate this with anything like lastpass, no external services.
Keepass integration would be nice though.




