#!/bin/bash

tag=$1

docker tag drive-gooder-base:"$tag" halzinnia/drive-gooder-base:"$tag"
docker tag drive-gooder-container-repository:"$tag" "$ECR_URI"/drive-gooder-container-repository:latest

docker push halzinnia/drive-gooder-base:"$tag"