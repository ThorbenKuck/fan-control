#!/bin/bash

curl -s https://api.github.com/repos/ThorbenKuck/fan-control/releases | jq '.[] | {published_at: .published_at, download: .zipball_url}'