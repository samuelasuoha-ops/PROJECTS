# Terraform: ECR + ECS (Fargate) + ALB

This module provisions a minimal AWS stack to run your Dockerized Python app on **ECS Fargate** behind an **Application Load Balancer**, plus an **ECR repository** for your images.

## What it creates
- VPC with 2 public subnets (for simplicity)
- Security groups for ALB and ECS service
- ALB + Target Group + Listener (HTTP:80)
- ECS Cluster (Fargate) + Task Execution Role + Task Role
- CloudWatch Log Group for the container
- ECS Task Definition & Service (Fargate)
- ECR Repository

## Prerequisites
- Terraform installed
- AWS credentials configured (e.g., via `aws configure`)
- Choose a region that supports Fargate (e.g., `eu-west-1`).

## Usage
```bash
terraform init
terraform plan -out tfplan
terraform apply tfplan
```

Set variables via `-var` flags or copy `terraform.tfvars.example` to `terraform.tfvars` and edit.

After apply:
- Get the **ALB DNS name** from outputs, e.g. `http://<alb_dns_name>`
- The service expects the app to expose port **8000**.

## Deploy flow with GitHub Actions
1. Terraform creates **ECR**, **ECS Cluster**, **ECS Service**, and **ALB**.
2. Your GitHub Actions workflow builds & pushes an image to ECR.
3. (Optional) The workflow updates the ECS service using the provided task definition file (or you can set `image_uri` and `terraform apply` to roll out).

> For first-time apply, set `image_uri` to a valid ECR image (or a placeholder) to create the ECS Service. Future updates can be handled by GitHub Actions' ECS deploy step.
