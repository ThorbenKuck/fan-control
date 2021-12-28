#!/bin/bash

payload=$(curl -s https://api.github.com/repos/ThorbenKuck/fan-control/releases | jq '.[0] | {published_at: .published_at, download: .zipball_url}')
published_at=$(echo "$payload" | jq -r '.published_at')
download_url=$(echo "$payload" | jq -r '.download')
echo "$published_at"
echo "$download_url"

last_release="$(cat "/opt/fan-control/meta-inf/released")"
#last_release=$(cat "../meta-inf/released")

if [[ "$published_at" > "$last_release" ]]; then
  target_file=/opt/fan-control/download/$published_at.zip
#  target_file=./$published_at.zip
  echo "Downloading newest version"
  curl "$download_url" --output "$target_file"

  work_dir=$(mktemp -d)
  unzip "$target_file" "$work_dir"
  cd "$work_dir" || exit 12
  ./install
  cd /opt/fan-control/ || exit 12
  rm -rf "$work_dir"
fi
