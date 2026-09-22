output "vpc_id" {
  value = module.vpc.vpc_id
}

output "private_subnet_ids" {
  value = module.vpc.private_subnets
}

output "public_subnet_ids" {
  value = module.vpc.public_subnets
}

output "availability_zones" {
  value = module.vpc.azs
}

output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "eks_cluster_version" {
  value = module.eks.cluster_version
}

output "eks_oidc_provider_arn" {
  value = module.eks.oidc_provider_arn
}

output "eks_managed_node_groups" {
  value = module.eks.eks_managed_node_groups
}
