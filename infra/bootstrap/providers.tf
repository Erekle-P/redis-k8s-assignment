provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "redis-k8s-assignment"
      Environment = "dev"
      ManagedBy   = "Terraform"
    }
  }
}
