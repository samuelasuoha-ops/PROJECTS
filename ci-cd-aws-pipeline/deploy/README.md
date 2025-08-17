# Deploy Scripts

- `ecr_push.sh` — Example script to build, tag, and push a Docker image to **Amazon ECR** using AWS CLI.
- `ec2_deploy.sh` — Example script to pull and run the image on an **EC2 host** via SSH/Docker.
- `ecs-task-def.json` — Template ECS task definition referencing an ECR image.

> Adjust repository names, regions, account IDs, and ARNs for your environment.
