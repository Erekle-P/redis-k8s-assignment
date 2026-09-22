from fastapi import FastAPI, HTTPException, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
import os
import time

import redis

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)


@app.middleware("http")
async def observe_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start

    if request.url.path != "/metrics":
        REQUEST_COUNT.labels(
            method=request.method,
            path=request.url.path,
            status=str(response.status_code),
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            path=request.url.path,
        ).observe(elapsed)

    return response


@app.get("/")
def root():
    return {"message": "FastAPI is working"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def ready():
    try:
        r.ping()
        return {"status": "ready"}
    except redis.RedisError as exc:
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable",
        ) from exc


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.post("/cache")
def store_value(key: str, value: str):
    r.set(key, value)
    return {"message": f"Stored key '{key}'"}


@app.get("/cache")
def get_value(key: str):
    value = r.get(key)

    if value is None:
        raise HTTPException(
            status_code=404,
            detail="Key not found",
        )

    return {
        "key": key,
        "value": value.decode(),
    }
