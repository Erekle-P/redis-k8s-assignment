terraform {
  backend "s3" {
    key          = "redis-k8s-assignment/dev/terraform.tfstate"
    use_lockfile = true
    encrypt      = true
  }
}
