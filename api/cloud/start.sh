#!/usr/bin/env bash
service nginx start
uwsgi --ini cloud/uwsgi.ini -l 4096