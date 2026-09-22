# Kubernetes Rollout Strategy

The FastAPI Deployment uses Kubernetes `RollingUpdate`.

Configured behavior:

- `maxUnavailable: 0` — keep existing Ready capacity during a rollout.
- `maxSurge: 1` — allow one additional Pod while replacing the old revision.
- `minReadySeconds: 5` — require a new Pod to remain Ready before it is considered available.
- `revisionHistoryLimit: 5` — keep recent ReplicaSets for rollback.

Useful commands:

```bash
kubectl rollout status deployment/python-api
kubectl rollout history deployment/python-api
kubectl rollout undo deployment/python-api
```

Kubernetes also supports `Recreate`, which terminates the previous Pods before starting the replacement. The application uses RollingUpdate because the API is expected to remain available during normal deployments.
