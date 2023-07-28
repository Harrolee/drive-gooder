#!/usr/bin/env bash
service nginx start
uwsgi --ini uwsgi.ini -l 4096