#!/bin/bash

pgrep -x fan-server >/dev/null && echo "The fan-server is still running. Please stop it before you continue"; exit 12 || echo "Starting the fan-server"

log_target=/dev/null

while getopts l flag
do
    case "${flag}" in
        l) log_target=${OPTARG};;
        *) echo "Unknown flag ${flag}. Please use -l to define the target for the logs (default /dev/null)"; exit 1;;
    esac
done

nohup bash -c 'exec -a fan-server /opt/fan-control/start-fan-server.sh' >"$log_target" 2>&1 &
