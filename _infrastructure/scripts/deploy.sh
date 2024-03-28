#! /bin/bash
set -e

CONTAINER_TAG=latest
export CONTAINER_TAG

cd web || exit 1


# Build and run Dockerfile
cd api || exit 1

docker build . -f cloud/Dockerfile -t drive-gooder-container-repository:"${CONTAINER_TAG}".

docker run -d \
  -p 80:80 \
  -p 443:443 \
  --env-file .env \
  --name devtest \
  --mount type=bind,readonly,source=./sslCert,target=/etc/nginx/certs \
  drive-gooder-container-repository:"${CONTAINER_TAG}"