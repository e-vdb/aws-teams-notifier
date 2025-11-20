provider "aws" {
  region = var.aws_region
  profile = "terraformuser"

  default_tags {
    tags = {
      Owner       = var.owner
      Client      = var.client
      Project     = var.project_name
      Environment = var.environment
    }
  }
}
