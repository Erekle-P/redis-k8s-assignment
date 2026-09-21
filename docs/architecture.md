# Architecture Review — Local Platform

## Request path

```text
Client
  |
  +--> NGINX Ingress :80
  |      |
  |      v
  |   python-api Service
  |
  +--> Istio Ingress Gateway :8083 (port-forward in local lab)
         |
         v
      Gateway + VirtualService
         |
         v
      python-api Service
         |
         v
      FastAPI Pod + Envoy
         |
         v
      Redis Service
         |
         v
      Redis Pod + Envoy
         |
         v
      PersistentVolumeClaim
```

## Delivery path

```text
GitHub main
   |
   v
Argo CD
   |
   v
Helm chart rendering
   |
   v
Kubernetes desired state
```

## Local-to-AWS mapping

| Local | AWS |
|---|---|
| kind | Amazon EKS |
| local Docker image | Amazon ECR |
| kind node | EKS managed node group |
| NGINX Ingress | AWS Load Balancer Controller / ALB |
| local persistent volume | EBS-backed Kubernetes storage |
| local GitOps | Argo CD on EKS |
| local Istio | Istio on EKS |

This checkpoint closes the local-platform portion of the assignment.
