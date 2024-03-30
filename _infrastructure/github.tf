locals {
 ecr_repo_name = "drive-gooder-final"
 AWS_TOKEN_KEY = "AKIAUQWTAUZKCH3RP4F4"
}

data "github_repository" "repo" {
  full_name = "harrolee/drive-gooder"
}

resource "github_repository_environment" "this" {
  repository = data.github_repository.repo.name
  environment = "sandbox"
}

resource "github_actions_environment_variable" "envvar_aws_region" {
  repository = data.github_repository.repo.name
  environment = github_repository_environment.this.environment
  variable_name = "AWS_REGION"
  value = "us-east-2"
}

resource "github_actions_environment_variable" "envvar_ecr_repository" {
  repository = data.github_repository.repo.name
  environment = github_repository_environment.this.environment
  variable_name = "ECR_REPOSITORY"
  value = local.ecr_repo_name
}

resource "github_actions_environment_variable" "envvar_aws_access_key_id" {
  repository = data.github_repository.repo.name
  environment = github_repository_environment.this.environment
  variable_name = "AWS_ACCESS_KEY_ID"
#   value = var.AWS_TOKEN_KEY
  value = local.AWS_TOKEN_KEY
}