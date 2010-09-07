#! /bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

pwd=$(pwd)
date=$(date +%Y%m%d)

(cd $tmp
cvs -q -d:pserver:anonymous@project-x.cvs.sourceforge.net:/cvsroot/project-x \
  co -D $date -d ProjectX-0.90.4.00-${date}cvs Project-X)
tar --create --xz \
  --exclude-vcs --exclude=lib --exclude '*.cmd' --exclude '*.bat' \
  --file=ProjectX-0.90.4.00-${date}cvs.tar.xz \
  --directory=$tmp ProjectX-0.90.4.00-${date}cvs
