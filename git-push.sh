#!/bin/sh

if [ "${1}" = "" ]; then
    MESSAGE="update"
fi

git add .
git commit -m $MESSAGE
git push