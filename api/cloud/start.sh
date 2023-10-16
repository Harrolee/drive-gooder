#!/usr/bin/env bash
set -e

# www-data will run nginx
nginx -t
service nginx start

# appUser runs app
head -n 3 /home/appUser/.bashrc
su appUser -c "bash appUserStart.sh"
