#!/usr/bin/env bash
set -e

# www-data will run nginx
nginx -t
service nginx start

# appUser runs app
su appUser -c "bash appUserStart.sh"
