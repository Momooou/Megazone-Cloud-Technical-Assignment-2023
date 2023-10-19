terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.21.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.3.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.2.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "2.4.0"
    }
  }

  required_version = "~> 1.0"
}

provider "aws" {
  region  = "ap-east-1"
  profile = "morrischan"
}
