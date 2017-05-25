#!/bin/bash
while read -r pkg_name; do
    gpg --armor --detach-sign "${pkg_name}"
done < <( find ./dist -type f -name \*.tar.gz )
while read -r pkg_name; do
    gpg --armor --detach-sign "${pkg_name}"
done < <( find ./dist -type f -name \*.whl )
