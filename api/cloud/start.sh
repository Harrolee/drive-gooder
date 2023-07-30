#!/usr/bin/env bash
service nginx start
source ./.venv/bin/activate
whoami
uwsgi --ini cloud/uwsgi.ini -l 4096 