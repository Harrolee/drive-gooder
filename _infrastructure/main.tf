terraform {
  required_version = "~> 1.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.42.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
  profile = "lee-solo"
  default_tags {
    tags = { terraform = "true", app = "drive-gooder" }
  }
}

locals {
  container_image = "310753928788.dkr.ecr.us-east-2.amazonaws.com/drive-gooder-final:latest"
  container_name = "drive-gooder-container"

  secret_arn = "arn:aws:secretsmanager:us-east-2:310753928788:secret:drive-gooder-secrets-5lmhvt"

  # use list after tutorial
  container_port_http = 80
  container_port_https = 443
}

# * Give Docker permission to pusher Docker images to AWS
# data "aws_caller_identity" "this" {}
# data "aws_ecr_authorization_token" "this" {}
# data "aws_region" "this" {}
# locals { ecr_address = format("%v.dkr.ecr.%v.amazonaws.com", data.aws_caller_identity.this.account_id, data.aws_region.this.name) }
# provider "docker" {
#  registry_auth {
#   address  = local.ecr_address
#   password = data.aws_ecr_authorization_token.this.password
#   username = data.aws_ecr_authorization_token.this.user_name
#  }
# }


## AppRunner
resource "aws_apprunner_service" "this" {
  service_name = "drive-gooder"
  source_configuration {
    image_repository {
      image_configuration {
        port = "80"
        runtime_environment_variables = {
          OPENAI_API_KEY="replace me"
          SUMMARIZE_MODEL="hosted_openai"
          SPEECH_TO_TEXT_MODEL="hosted_openai"
          QUESTION_MODEL="hosted_openai"
          TEXT_TO_SPEECH_MODEL="local_coqui"
          GOOGLE_CLIENT_ID="73232257368-9v4kp1o2c5tptr5h13h6k5tql6483kc6.apps.googleusercontent.com"
          GOOGLE_CLIENT_SECRET="replace-me"
          ROOT_URI="https://localhost/"
        }
        # get the arns from secret manager
        # runtime_environment_secrets = {
        #   GOOGLE_CLIENT_SECRET=
        #   OPENAI_API_KEY=
        # }
      }
      image_identifier      = local.container_image
      image_repository_type = "ECR"
    }
    auto_deployments_enabled = true
    authentication_configuration {
      access_role_arn = aws_iam_role.ecrAccessorRole.arn
    }
  }
  # what is instance_configuration?
  instance_configuration {
    # instance_role_arn = aws_iam_role.secret_reader.arn
    cpu = "1024"
    memory = "2048"
  }
  auto_scaling_configuration_arn = aws_apprunner_auto_scaling_configuration_version.this.arn
  # I don't think I need this until I add services for drive-gooder to connect to
    # like a db, or an s3 bucket
  # network_configuration {
  #   egress_configuration {
  #     egress_type = "VPC"
  #     vpc_connector_arn = aws_apprunner_vpc_connector.connector.arn
  #   }
  # }
  health_check_configuration {
    # change drive-gooder healthcheck endpoint to return a 200 instead of a 301
    path = "/api"
  }
}

resource "aws_apprunner_auto_scaling_configuration_version" "this" {
  auto_scaling_configuration_name = "drive-gooder-scaling"

  max_concurrency = 1
  max_size        = 1
  min_size        = 1
}


## AppRunner Permissions

# allow access to secrets in secret manager
# resource "aws_iam_role" "secret_reader" {
#   name = "drive-gooder-apprunner-secret-reader-role"
#   assume_role_policy = data.aws_iam_policy_document.apprunner_assume_role_policy.json
  
#   inline_policy {
#     name = "read-secrets-policy"
#     policy = jsonencode({
#       Statement = [{
#         Action   = [
#           "secretsmanager:GetRandomPassword",
#           "secretsmanager:GetResourcePolicy",
#           "secretsmanager:GetSecretValue",
#           "secretsmanager:DescribeSecret",
#           "secretsmanager:ListSecretVersionIds",
#           "secretsmanager:ListSecrets",
#           "secretsmanager:BatchGetSecretValue"
#         ]
#         Effect   = "Allow"
#         Resource = "*"
#         # Principal = {
#         #     Service = "tasks.apprunner.amazonaws.com"
#         # }
#         # ? ["tasks.apprunner.amazonaws.com", "build.apprunner.amazonaws.com", "apprunner.amazonaws.com"]
#       }]
#       Version   = "2012-10-17"
#     })
#   }
# }

## allow access to containers in ecr
resource "aws_iam_role" "ecrAccessorRole" {
  name               = "ecrAccessorRole"
  assume_role_policy = data.aws_iam_policy_document.apprunner_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "ecrAccessorRole_policy" {
  role       = aws_iam_role.ecrAccessorRole.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

data "aws_iam_policy_document" "apprunner_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["tasks.apprunner.amazonaws.com", "build.apprunner.amazonaws.com", "apprunner.amazonaws.com"]
    }
  }
}