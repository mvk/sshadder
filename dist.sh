#!/usr/bin/env bash
tox -e py27,py35 && python setup.py bdist_wheel
