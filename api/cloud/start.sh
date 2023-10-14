#!/usr/bin/env bash
set -e

chown -R www-data /app 
chown -R www-data /root

nginx -t
service nginx start
source ./.venv/bin/activate
uwsgi --ini uwsgi.ini -l 4096