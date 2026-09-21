provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "redis-k8s-assignment"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}
