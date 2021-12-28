#!/bin/bash

stop-fan-server

log_target=/dev/null

while getopts l flag
do
    case "${flag}" in
        l) log_target=${OPTARG};;
        *) echo "Unknown flag ${flag}. Please use -l to define the target for the logs (default /dev/null)"; exit 1;;
    esac
done

nohup bash -c 'exec -a fan_server /opt/fan-control/fan-server' >"$log_target" 2>&1 &
