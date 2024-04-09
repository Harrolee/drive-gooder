#!/bin/bash

tag=$1

docker tag drive-gooder-base:"$tag" halzinnia/drive-gooder-base:"$tag"
# docker tag drive-gooder-base:"$tag" "$ECR_URI"/drive-gooder-base:latest

docker push halzinnia/drive-gooder-base:"$tag"

docker buildx build . -f cloud/Base.Dockerfile --platform=linux/amd64  --push -t halzinnia/drive-gooder-base:v0.0.6amd
docker buildx build . -f cloud/Final.Dockerfile --platform=linux/amd64  --push -t halzinnia/drive-gooder-final:v0.0.6amd