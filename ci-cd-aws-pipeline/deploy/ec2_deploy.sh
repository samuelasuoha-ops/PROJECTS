#!/usr/bin/env bash
set -euo pipefail
# Example: SSH deploy to EC2 (host must have Docker installed)

EC2_HOST="${1:-ec2-user@your-ec2-host}"
ECR_IMAGE="${2:-123456789012.dkr.ecr.eu-west-1.amazonaws.com/python-ci-api:latest}"

ssh -o StrictHostKeyChecking=no "$EC2_HOST" bash -s <<'EOF'
set -euo pipefail
docker ps -q --filter "name=python-ci-api" | xargs -r docker stop
docker ps -aq --filter "name=python-ci-api" | xargs -r docker rm
docker pull 123456789012.dkr.ecr.eu-west-1.amazonaws.com/python-ci-api:latest
docker run -d --name python-ci-api -p 80:8000 123456789012.dkr.ecr.eu-west-1.amazonaws.com/python-ci-api:latest
EOF

echo "Deployed to $EC2_HOST"
