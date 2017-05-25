#!/usr/bin/env bash
git clean -fdx
tox -e py27,py35 && python setup.py sdist bdist_wheel
