#!/bin/bash

pgrep -x fan-client >/dev/null && echo "Stopping the fan-client" || echo "The fan-client is already terminated"; exit 0

pkill -f fan-client

pgrep -x fan-client >/dev/null && pkill -9 -f fan-client