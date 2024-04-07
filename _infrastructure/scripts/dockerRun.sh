#!/bin/bash

# for realz!!
docker run \
  -p 80:80 \
  -p 443:443 \
  --env-file .env \
  --name devtest \
  
# debugging
docker run \
  --entrypoint /bin/bash \
  -it \
  -p 80:80 \
  --env-file .env \
  --name devtest \
  does-it-work


# cross-platform build
docker buildx build . -f cloud/BaseImage.Dockerfile --platform=linux/amd64 --push -t halzinnia/drive-gooder-base:v0.0.5amd -t halzinnia/drive-gooder-base:latest
