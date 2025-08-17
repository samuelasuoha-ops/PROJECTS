# CI/CD Pipeline to AWS (Dockerized Python App)

Automated build and deploy for a containerized **Python/Flask** app using **GitHub Actions** and **Jenkins**, targeting **AWS** (ECR + ECS or EC2 via SSH).

## Tech
- Python, Flask
- Docker
- GitHub Actions
- Jenkins
- AWS (ECR, ECS or EC2)

---

## Project Structure
```
ci-cd-aws-pipeline/
  app/
    app.py
    requirements.txt
  Dockerfile
  docker-compose.yml
  Jenkinsfile
  .github/workflows/aws-ci.yml
  deploy/
    ecr_push.sh
    ec2_deploy.sh
    ecs-task-def.json
    README.md
```

---

## Option A — GitHub Actions → ECR → ECS
1. **Create an ECR repository** (e.g., `python-ci-api`).
2. **Set GitHub Secrets** in your repo:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION` (e.g., `eu-west-1`)
   - `ECR_REPOSITORY` (e.g., `python-ci-api`)
   - `ECS_CLUSTER` (e.g., `demo-cluster`)
   - `ECS_SERVICE` (e.g., `demo-service`)
3. **Push to `main`**. The workflow will:
   - Build the Docker image
   - Login to ECR and push the image
   - (Optional) Update ECS service to use the new image (rolling deploy)

> If you don’t have ECS yet, you can skip the ECS update step and only push to ECR.

---

## Option B — Jenkins → EC2 (SSH) or ECR/ECS
- Use the `Jenkinsfile` provided.
- Jenkins stages: Checkout → Build → Test → Docker Build → Push (optional) → Deploy (manual/SSH).

---

## Local Dev
```bash
docker-compose up --build
# http://localhost:8000/health
```

## API
- `GET /health` → `{"status":"ok"}`

---

## Notes
- **Never commit secrets.** Use GitHub Secrets/Jenkins credentials.
- The provided scripts are **reference templates**. Adjust resource names/ARNs, VPC configs, and IAM permissions for your environment.
- For production, consider IaC (Terraform/CloudFormation) and a proper ECS/ALB/VPC setup.
