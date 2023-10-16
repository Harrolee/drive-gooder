#!/usr/bin/env bash
set -e

groupadd --gid 1010 socketWriters
usermod -a -G socketWriters www-data

# create appUser
# gid 1010 is socketWriters
useradd -g 1010 -m -p $(cat password) appUser # create user with a home dir. Coqui saves models to the user's home dir
shred -u password

# set HOME on non-login user changes for appUser:
sed -i '1s;^;export HOME="/home/appUser"\n;' /home/appUser/.bashrc
sed -i '1s;^;echo "running bashrc for appUser"\n;' /home/appUser/.bashrc
sed -i '1s;^;source ./.venv/bin/activate\n;' /home/appUser/.bashrc

# Create the .local and share directories if useradd does not make them
if [ ! -d "/home/appUser/.local" ]; then
  mkdir -p "/home/appUser/.local/share/tts"
  # coqui seems to use both tts and tts-caches
  mkdir -p "/home/appUser/.local/share/tts-cache"
  chown -R appUser "/home/appUser/"
fi

# make appUser owner of /app. This operation takes a long time
chown -R appUser /app