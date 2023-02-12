#!/bin/sh

echo "cloning repo"
if [ ! -d archzfsdepends ] ; then
  git clone https://github.com/zUnixorn/archzfsdepends.git archzfsdepends
else
  cd archzfsdepends
fi


echo "git repo seems to belong to another user, this should fix it (https://stackoverflow.com/questions/72978485)"
git config --global --add safe.directory '*'

echo "checking out repo"
git checkout github-pages

echo "making repo dir"
mkdir -p zfsdepends

echo "running python script"
python /archzfs_synchronize.py

echo "setting username and user email"
git config --global user.name "zUnixorn"
git config --global user.email "dev@jonascrull.de"

echo "adding repo"
git add *

echo "commiting packages"
git commit -m "updated repo"

echo "pushing"
git push
