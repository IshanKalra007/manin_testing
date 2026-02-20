#!/bin/bash
# Build and push renderer to AWS ECR
# Usage: ./deploy.sh <aws-account-id> <region>

set -e

AWS_ACCOUNT_ID=${1:-$(aws sts get-caller-identity --query Account --output text)}
AWS_REGION=${2:-us-east-1}
REPO_NAME=vynotes-manim-renderer
IMAGE_TAG=latest

echo "Building Docker image..."
docker build -t $REPO_NAME .

echo "Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

echo "Creating ECR repo if not exists..."
aws ecr describe-repositories --repository-names $REPO_NAME --region $AWS_REGION 2>/dev/null || \
  aws ecr create-repository --repository-name $REPO_NAME --region $AWS_REGION

FULL_IMAGE=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG
docker tag $REPO_NAME:latest $FULL_IMAGE

echo "Pushing to ECR..."
docker push $FULL_IMAGE

echo "Done! Image: $FULL_IMAGE"
echo ""
echo "Run on EC2 with:"
echo "  docker run -d -p 8000:8000 -e S3_BUCKET=your-bucket -e AWS_REGION=$AWS_REGION $FULL_IMAGE"
