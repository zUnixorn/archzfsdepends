#!/bin/sh

git clone git@github.com:zUnixorn/archzfsdepends.git
cp archzfsdepends/archzfs_synchronize.py .
cd archzfsdepends
git checkout github-pages
mkdir -p zfsdepends
python ../archzfs_synchronize.py
git commit -m "updated repo"
git push
