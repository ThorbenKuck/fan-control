#!/bin/bash

while getopts s:c:a flag
do
    case "${flag}" in
        s) server=true;;
        c) client=true;;
        a) server=true;client=true;;
        *) echo "Unknown flag ${flag}. Please use -s to build the server, -c to build the client or -a to build both"; exit 1;;
    esac
done

rm -rf src/
mkdir src/
cp ./*.py src/
cp types/ src/
cp manifest src/

# shellcheck disable=SC2164
cd src/

while read -r line; do pip install "$line"; done < manifest

rm -rf dist/ build/ fan-server.spec fan-client.spec

if [ "$server" ]; then
  pyinstaller -F fan-server.py
  cp dist/fan-server ../fan-server
fi

if [ "$client" ]; then
  pyinstaller -F fan-client.py
  cp dist/fan-client ../fan-client
fi

rm -rf build/