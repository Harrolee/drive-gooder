# Drive Gooder

# Setup

* Install `ffmpeg`
* Install Python 3.x
* Install `espeak`
* Install `mecab` (at least on M1 Macs)
* Install `poetry` (`pip install poetry`)


# Docker
## Build Container
docker build . -f cloud/Dockerfile -t drive-gooder-container-repository:{tag}

## Run Container Locally
docker run -d -p 5003:5003 --env-file test.env drive-gooder-container-repository:{tag}

## Push Container to ECR
Will need to have the aws cli installed.
Recommened to look at the `View push commands` output for the ecr repository in AWS.

1.aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin {special-uri-for-ecr-instance}
1.docker tag drive-gooder-container-repository:{tag} {ecr-uri}:{tag}
1.docker push {ecr-uri}:{tag}

## Update ECS to use new container

1. Get to task definitions in [aws](https://us-east-2.console.aws.amazon.com/ecs/home?region=us-east-2#/taskDefinitions)
1. Go to the task currently named `first-run-task-definition`
1. Open up the latest revision
1. Click to `Create new revision`
1. Click on the container definition.
1. Change version in the image section.

## Add new Secret

1. Navigate to the secret manager in [aws](https://us-east-2.console.aws.amazon.com/secretsmanager/listsecrets?region=us-east-2)
1. Open up the defined secret.
1. In the `Secret Value` section click `Retrieve secret value`
1. Click `edit` and make necessary changes.
1. Update ecs by creating new task definition with new environment variable mapped to the new secret. (can follow instructions for update ECS to use new container)
