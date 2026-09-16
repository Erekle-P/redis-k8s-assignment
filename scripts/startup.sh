#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
K8S_DIR="${ROOT_DIR}/k8s"

kubectl apply -f "${K8S_DIR}/redis-configmap.yaml"
kubectl apply -f "${K8S_DIR}/redis-secret.yaml"
kubectl apply -f "${K8S_DIR}/redis-pvc.yaml"
kubectl apply -f "${K8S_DIR}/redis-deployment.yaml"
kubectl apply -f "${K8S_DIR}/redis-service.yaml"
kubectl apply -f "${K8S_DIR}/deployment.yaml"
kubectl apply -f "${K8S_DIR}/service.yaml"
kubectl apply -f "${K8S_DIR}/ingress.yaml"

kubectl get pods
kubectl get svc
kubectl get ingress
