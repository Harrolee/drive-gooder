#!/bin/bash

tag=$1
AWS_SSO_PROFILE=lee-solo
ECR_URI=310753928788.dkr.ecr.us-east-2.amazonaws.com

docker tag drive-gooder-container-repository:"$tag" "$ECR_URI"/drive-gooder-container-repository:"$tag"
docker tag drive-gooder-container-repository:"$tag" "$ECR_URI"/drive-gooder-container-repository:latest

aws ecr get-login-password --region us-east-2 --profile "$AWS_SSO_PROFILE" | docker login --username AWS --password-stdin "$ECR_URI"
docker push "$ECR_URI"/drive-gooder-container-repository -a