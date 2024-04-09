#!/usr/bin/env bash
set -e

source ./.venv/bin/activate
uwsgi --ini uwsgi.ini #-l 4096
                        # need to learn how to run the below in the App Runner environment
                        # echo 4096 > /proc/sys/net/core/somaxconn