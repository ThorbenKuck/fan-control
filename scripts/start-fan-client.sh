#!/bin/bash

pgrep -x fan-client >/dev/null && echo "The fan-client is still running. Please stop it before you continue"; exit 12 || echo "Starting the fan-client"

log_target=/dev/null

while getopts l flag
do
    case "${flag}" in
        l) log_target=${OPTARG};;
        *) echo "Unknown flag ${flag}. Please use -l to define the target for the logs (default /dev/null)"; exit 1;;
    esac
done

nohup bash -c 'exec -a fan-client /opt/fan-control/start-fan-client.sh' >"$log_target" 2>&1 &