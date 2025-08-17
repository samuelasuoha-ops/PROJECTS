#!/usr/bin/env bash
set -euo pipefail

# Requirements: awscli, docker, logged-in AWS account with ECR permissions
# Usage: ./ecr_push.sh <aws_account_id> <region> <repository> <image_tag>
ACCOUNT_ID="${1:-123456789012}"
REGION="${2:-eu-west-1}"
REPO="${3:-python-ci-api}"
TAG="${4:-latest}"

aws ecr describe-repositories --repository-names "$REPO" --region "$REGION" >/dev/null 2>&1 ||   aws ecr create-repository --repository-name "$REPO" --region "$REGION" >/dev/null

aws ecr get-login-password --region "$REGION" |   docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

docker build -t "$REPO:$TAG" .
docker tag "$REPO:$TAG" "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:$TAG"
docker push "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:$TAG"

echo "Pushed: $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:$TAG"
