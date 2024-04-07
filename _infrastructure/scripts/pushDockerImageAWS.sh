#!/bin/bash

tag=$1
AWS_SSO_PROFILE=lee-solo
ECR_URI=310753928788.dkr.ecr.us-east-2.amazonaws.com

docker tag drive-gooder-base:"$tag" "$ECR_URI"/drive-gooder-base:"$tag"
docker tag drive-gooder-base:"$tag" "$ECR_URI"/drive-gooder-base:latest

aws ecr get-login-password --region us-east-2 --profile "$AWS_SSO_PROFILE" | docker login --username AWS --password-stdin "$ECR_URI"
# docker push "$ECR_URI"/drive-gooder-container-repository -a
docker push "$ECR_URI"/drive-gooder-final -a


# build amd image from macbook and push to ECR
# docker buildx build . -f cloud/Final.Dockerfile --platform=linux/amd64 --push -t "$ECR_URI"/drive-gooder-final:latest




docker buildx build . -f cloud/Test.Dockerfile --platform=linux/amd64  --push -t "$ECR_URI"/drive-gooder-final:test-nginx

docker buildx build . -f cloud/lite.Dockerfile --platform=linux/amd64  --push -t "$ECR_URI"/drive-gooder-final:nginx-lite