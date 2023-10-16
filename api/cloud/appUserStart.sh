#!/usr/bin/env bash
source ./.venv/bin/activate
uwsgi --ini uwsgi.ini -l 4096