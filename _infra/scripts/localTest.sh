#!/bin/bash

docker build . -f cloud/Final.Dockerfile -t test-nginx

docker run \
  -p 3000:3000 \
  --env-file .env \
  --name devtest \
  test-nginx 