output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = aws_lb.app_alb.dns_name
}

output "ecr_repo_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.app_repo.repository_url
}

output "cluster_name" {
  value = aws_ecs_cluster.app_cluster.name
}

output "service_name" {
  value = aws_ecs_service.app_service.name
}

output "task_definition_arn" {
  value = aws_ecs_task_definition.app_task.arn
}
