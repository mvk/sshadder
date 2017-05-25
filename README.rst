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

* aims at *command line* only, no graphic desktop/dependency. no DBus (no need)
* does not compete with full-on private keys managers like Seahorse_
* ``ssh-agent`` management. You run it, and have ``SSH_AUTH_SOCK`` properly pointing to the desired SSH Agent process


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

The text will guide you to give a master password (not saved anywhere), and then iterate over

* key file path
* key password

When you're ready, choose 's' option to save and quit.

What is actually happening
--------------------------

Given config file ``.sshagent.json`` and master password, the utility adds all the ssh key files using their passwords ``JSON`` file keeps the key passwords encrypted using simple-crypt package.
Each password is encrypted and then encoded using ``Base64`` and added to the key item.
The text file is kept as it is now - text file.

Not sure how REALLY safe it is, but it is safer than plain text shell scripts.


Current known security problems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As long as ``pexpect.spawn()`` is used here, it means if your system is compromised and rogue user can access your ``/proc``, they probably can see the passwords passed to ssh-agent in clear text.
If this is VERY unsafe for you, please send a patch/pull request :)


Contributing
============

Patches/pull/feature requests are welcome to improve the code/fix bugs.
Note I'm quite a busy person, so if you can fix/add it - send me a patch/pull-request.


.. _SeaHorse: https://wiki.gnome.org/Apps/Seahorse

