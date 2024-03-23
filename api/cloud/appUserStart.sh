#!/usr/bin/env bash
set -e

source ./.venv/bin/activate
uwsgi --ini uwsgi.ini -l 4096