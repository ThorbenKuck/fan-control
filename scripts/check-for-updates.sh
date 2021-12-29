#!/bin/bash

payload=$(curl -s https://api.github.com/repos/ThorbenKuck/fan-control/releases | jq '.[0] | {published_at: .published_at, download: .zipball_url}')
published_at=$(echo "$payload" | jq -r '.published_at')
download_url=$(echo "$payload" | jq -r '.download')
last_known_release="$(cat "/opt/fan-control/meta-inf/released")"

server_running=false
client_running=false

pgrep -x "fan-server" >/dev/null && server_running=true
pgrep -x "fan-client" >/dev/null && client_running=true

echo "[SERVER]: $published_at"
echo "[LOCAL]: $last_known_release"

#last_known_release=$(cat "../meta-inf/released")

if [[ "$published_at" > "$last_known_release" ]]; then
  echo "[INFO]: Found new version!"
  target_file=/opt/fan-control/download/$published_at.zip
#  target_file=./$published_at.zip
  echo "[INFO]: Downloading newest version .."
  sudo curl -L "$download_url" --output "$target_file"
  echo "[INFO]: Newest version downloaded. Creating temp folder"

  work_dir="$(mktemp -d)"
  echo "[INFO]: Unzipping newly downloaded version"
  sudo unzip -d "$work_dir" "$target_file"
  echo "[INFO]: Installing newest version through provided install script"
  cd "$work_dir" || exit 12
  cd ./* || exit 13
  sudo bash "install"
  echo "[INFO]: Done installing"
  cd /opt/fan-control/ || exit 12
  echo "[INFO]: Clearing work directory"
  sudo rm -rf "$work_dir"
  sudo bash -c 'printf "%s" "$published_at" >/opt/fan-control/meta-inf/released'

  if [ "$server_running" ]; then
    sudo bash "start-fan-server.sh"
  fi
  if [ "$client_running" ]; then
    sudo bash "start-fan-client.sh"
  fi
fi
