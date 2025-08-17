variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "vpc_cidr" {
  description = "CIDR for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "Two public subnet CIDRs"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "app_name" {
  description = "App/service name"
  type        = string
  default     = "python-ci-api"
}

variable "ecr_repo_name" {
  description = "ECR repository name"
  type        = string
  default     = "python-ci-api"
}

variable "cluster_name" {
  description = "ECS cluster name"
  type        = string
  default     = "demo-cluster"
}

variable "desired_count" {
  description = "Desired number of tasks"
  type        = number
  default     = 1
}

variable "image_uri" {
  description = "Full image URI (e.g., ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/REPO:TAG)"
  type        = string
  default     = "ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/python-ci-api:latest"
}
