#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Cleaning $(dirname "$0")"

# echo "Files to be deleted:"
# find -mindepth 1 -maxdepth 1 ! -name 'clean.sh' -type f

# echo -n "Continue (y/n)? "
# read answer
answer="y"
if [ "$answer" != "${answer#[Yy]}" ] ;then
    # echo Yes
    find -mindepth 1 -maxdepth 1 ! -name 'clean.sh' -type f -print0 | xargs -r0 rm -R
else
    echo No
fi