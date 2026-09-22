pipeline {
  agent any

  environment {
    AWS_REGION = 'us-east-1'
    ECR_REPOSITORY = 'redis-fastapi'
  }

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  stages {
    stage('Validate') {
      steps {
        sh '''#!/usr/bin/env bash
set -euo pipefail
python3 -m compileall -q app.py
helm lint helm/python-api
'''
      }
    }

    stage('Build Image') {
      steps {
        sh '''#!/usr/bin/env bash
set -euo pipefail
SHORT_SHA="$(git rev-parse --short HEAD)"
IMAGE_TAG="ci-$BUILD_NUMBER-$SHORT_SHA"
printf '%s' "$IMAGE_TAG" > .ci-image-tag
docker build -t "python-api:$IMAGE_TAG" .
'''
      }
    }

    stage('Smoke Test') {
      steps {
        sh '''#!/usr/bin/env bash
set -euo pipefail
IMAGE_TAG="$(cat .ci-image-tag)"
CONTAINER="python-api-ci-$BUILD_NUMBER"

cleanup() {
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker run -d --name "$CONTAINER" -p 18000:8000 "python-api:$IMAGE_TAG" >/dev/null

for attempt in {1..20}; do
  if curl -fsS http://127.0.0.1:18000/health >/dev/null; then
    curl -fsS http://127.0.0.1:18000/health
    exit 0
  fi
  sleep 1
done

docker logs "$CONTAINER"
exit 1
'''
      }
    }

    stage('Push to ECR') {
      steps {
        sh '''#!/usr/bin/env bash
set -euo pipefail
IMAGE_TAG="$(cat .ci-image-tag)"

ECR_REPO="$(aws ecr describe-repositories \
  --repository-names "$ECR_REPOSITORY" \
  --region "$AWS_REGION" \
  --query 'repositories[0].repositoryUri' \
  --output text)"

ECR_REGISTRY="${ECR_REPO%/*}"

aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$ECR_REGISTRY" >/dev/null

docker tag "python-api:$IMAGE_TAG" "$ECR_REPO:$IMAGE_TAG"
docker push "$ECR_REPO:$IMAGE_TAG"

printf '%s\n' "$ECR_REPO:$IMAGE_TAG" > image-reference.txt
printf '%s' "$ECR_REPO" > .ci-ecr-repo
'''
      }
    }

    stage('Update GitOps Manifest') {
      steps {
        sh '''#!/usr/bin/env bash
set -euo pipefail

IMAGE_TAG="$(cat .ci-image-tag)"
ECR_REPO="$(cat .ci-ecr-repo)"
VALUES_FILE="helm/python-api/values-eks.yaml"

python3 scripts/update_gitops_values.py "$VALUES_FILE" "$ECR_REPO" "$IMAGE_TAG"

git config user.name "Jenkins CI"
git config user.email "jenkins-ci@users.noreply.github.com"

git add "$VALUES_FILE"

if git diff --cached --quiet; then
  echo "GitOps values already point to this image."
  exit 0
fi

git commit -m "Deploy $IMAGE_TAG via GitOps"
git push origin HEAD:main
'''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'image-reference.txt', allowEmptyArchive: true
      sh '''#!/usr/bin/env bash
docker rm -f "python-api-ci-$BUILD_NUMBER" >/dev/null 2>&1 || true
'''
    }
  }
}
