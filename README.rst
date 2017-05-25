========
SSHAdder
========

.. image:: https://github.com/mvk/sshadder/raw/master/logo.200x200.png
    :target: https://github.com/mvk/sshadder



About
=====

.. image:: https://travis-ci.org/mvk/sshadder.svg?branch=master
    :target: https://travis-ci.org/mvk/sshadder

ssh keys manager for multiple password protected keys.
Stop adding them manually.


What it does
------------

Defines key bundles and allows adding all of keys in the bundle to a running ssh-agent

What it does not
----------------

* graphic desktop support or D-Bus
* compete with full-on private keys managers like Seahorse_
* manage ``ssh-agent``


Installation
============

Run in virtualenv: ::

    pip install sshadder


NOTE: The crypto path is not yet vetted, so do not install this system-wide just yet. Honestly :)


Usage
=====

Prerequisites:
--------------

Running and visible ``ssh-agent``

Normally:
---------

Run: ::

    sshadder

Please refer to ``--help``, which shows default locations it's looking for the JSON files.


Initialization:
---------------

Run: ::

    sshadder -i

The text will guide you to give a master password (not saved anywhere), and then for each key you wish to add, enter:

* file path
* password

When you're done, choose 's' option to save and quit.

What is actually happening
--------------------------

Upon invocation in normal mode, ``sshadder`` is:

1. checking ssh-agent environment variable is pointing to something useful
1. iterating over configuration file ``.sshagent.json`` entries and is adding the keys you have added.

The key passwords are encrypted, so master password is used to decrypt them to add them to the running agent.
Each password is encrypted and then encoded using ``Base64`` and added to the key item.
The text file is kept as it is now - text file.

Not sure how REALLY safe it is, but it is safer than plain text shell scripts.


Transparency
~~~~~~~~~~~~

``pexepect.spawn()`` is used, which means: 
Being able to access your user's ``/proc`` filesystem at the time of adding the keys can allow unauthorized access to your passwords. 
An attacker could possibly "sniff" file descriptors to see the passwords passed to ssh-agent upone each key. 
If this is VERY unsafe for you, please send a patch/pull request :) 

IF a security expert is reading these lines, I would like to learn how to avoid this


Contributing
============

Patches/pull/feature requests are welcome to improve the code/fix bugs.
Note I'm quite a busy person, so if you can fix/add it - send me a patch/pull-request.

.. _SeaHorse: https://wiki.gnome.org/Apps/Seahorse

