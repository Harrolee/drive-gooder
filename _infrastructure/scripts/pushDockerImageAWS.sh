#!/bin/bash

TAG=$1
AWS_SSO_PROFILE=lee-solo
ECR_URI=310753928788.dkr.ecr.us-east-2.amazonaws.com

aws ecr get-login-password --region us-east-2 --profile "$AWS_SSO_PROFILE" | docker login --username AWS --password-stdin "$ECR_URI"

docker buildx build . -f cloud/Final.Dockerfile --platform=linux/amd64  --push      \
-t 310753928788.dkr.ecr.us-east-2.amazonaws.com/drive-gooder-final:latest           \
-t 310753928788.dkr.ecr.us-east-2.amazonaws.com/drive-gooder-final:"$TAG"