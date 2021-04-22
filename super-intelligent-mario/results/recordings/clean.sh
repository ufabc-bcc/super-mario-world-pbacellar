#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Cleaning $(dirname "$0")"

# echo "folders to be deleted:"
# find -mindepth 1 -maxdepth 1 -type d

# echo -n "Continue (y/n)? "
# read answer
answer="y"
if [ "$answer" != "${answer#[Yy]}" ] ;then
    # echo Yes
    find -mindepth 1 -maxdepth 1 -type d -print0 | xargs -r0 rm -R
else
    echo No
fi