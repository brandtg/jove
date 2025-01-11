#!/bin/bash
set -Eeuxo pipefail

FILE=setup.py

# Find the current version
CURRENT=$(grep "version=" setup.py | perl -p -e 's/.*version="([\d.]+)".*/\1/')
CURRENT_MAJOR=$(echo $CURRENT | perl -p -e 's/(\d+)\.(\d+)\.(\d+)/\1/')
CURRENT_MINOR=$(echo $CURRENT | perl -p -e 's/(\d+)\.(\d+)\.(\d+)/\2/')
CURRENT_PATCH=$(echo $CURRENT | perl -p -e 's/(\d+)\.(\d+)\.(\d+)/\3/')

# Bump the patch version by 1
NEXT_PATCH=$(($CURRENT_PATCH + 1))
NEXT="$CURRENT_MAJOR.$CURRENT_MINOR.$NEXT_PATCH"

# Replace the version 
perl -p -i -e "s/version=\"$CURRENT\"/version=\"$NEXT\"/" $FILE
