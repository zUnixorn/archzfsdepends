#!/bin/sh

if [ ! -d archzfsdepends ] ; then
  git clone git@github.com:zUnixorn/archzfsdepends.git archzfsdepends
else
  cd archzfsdepends
fi

git checkout github-pages
mkdir -p zfsdepends
python /archzfs_synchronize.py
git commit -m "updated repo"
git push
