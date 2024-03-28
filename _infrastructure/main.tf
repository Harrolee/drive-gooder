terraform {
  required_version = "~> 1.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.42.0"
    }
  }
}

locals {
  container_name = "drive-gooder-container"
  # use list after tutorial
  container_port_http = 80
  container_port_https = 443
  example = "driveSafe"
}

provider "aws" {
  region = "us-east-2"

  default_tags {
    tags = { example = local.example }
  }
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