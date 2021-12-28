#!/bin/bash

pgrep -x fan-server >/dev/null && echo "Stopping the fan-server" || echo "The fan-server is already terminated"; exit 0

pkill -f fan-server

pgrep -x fan-server >/dev/null && pkill -9 -f fan-server
