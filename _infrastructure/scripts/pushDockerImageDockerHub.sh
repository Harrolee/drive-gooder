#!/bin/bash

tag=$1

docker tag drive-gooder-base:"$tag" halzinnia/drive-gooder-base:"$tag"
# docker tag drive-gooder-base:"$tag" "$ECR_URI"/drive-gooder-base:latest

docker push halzinnia/drive-gooder-base:"$tag"