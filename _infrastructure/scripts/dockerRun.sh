#!/bin/bash

# for realz!!
docker run \
  -p 80:80 \
  -p 443:443 \
  -p 44022:22 \
  --env-file .env \
  --name devtest \
  ssh-test
  # --mount type=bind,readonly,source=./sslCert,target=/etc/nginx/certs \
  # drive-gooder-container-repository:{tag}
  
# debugging
docker run \
  --entrypoint /bin/bash \
  -it \
  -p 80:80 \
  --env-file .env \
  --name devtest \
  --mount type=bind,readonly,source=./sslCert,target=/etc/nginx/certs \
  does-it-work