========
SSHAdder
========

.. image:: https://github.com/mvk/sshadder/raw/master/logo.200x200.png
    :target: https://github.com/mvk/sshadder



About
=====

.. image:: https://travis-ci.org/mvk/sshadder.svg?branch=master
    :target: https://travis-ci.org/mvk/sshadder

ssh keys manager for multiple password protected private keys written currently in Python. 
Stop adding them manually.


What it does
------------

Defines key bundles and allows adding all of keys in the bundle to a running ssh-agent 
In a way it is like GNU_Keychain_, but does not force you to type in all your passwords, thank you @jamiesonbecker!

What it does not
----------------

* graphic desktop, messaging a lá D-Bus and the likes
* compete with real private keys managers like Seahorse_, LastPass_, KeePass_
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

So that ``sshadder`` can work we need:

* Running process of ``ssh-agent``
* Environment variable ``SSH_AUTH_SOCK`` pointing to that running process

Setup:
------

Run: ::

    sshadder -i

The text will guide you to give a master password (not saved anywhere), and then for each key you wish to add, enter:

* file path
* password

When you're done, choose 's' option to save and quit.

Regular Use:
------------

Run: ::

    sshadder

Please refer to ``--help``, which shows default locations it's looking for the JSON files.


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


Related Tools:
==============

* SeaHorse_
* LastPass_
* GNU_Keychain_  


.. _SeaHorse: https://wiki.gnome.org/Apps/Seahorse
.. _LastPass: https://lastpass.com
.. _KeePass: http://keepass.info
.. _GNU_Keychain: http://www.funtoo.org/Keychain


