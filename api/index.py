from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

with open("telemetry.json") as f:
    data = json.load(f)

@app.post("/api")
async def latency_metrics(request: Request):
    body = await request.json()
    regions = body["regions"]
    threshold = body["threshold_ms"]

    result = {}

    for r in regions:
        records = [d for d in data if d["region"] == r]

        latencies = [d["latency_ms"] for d in records]
        uptimes = [d["uptime"] for d in records]

        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies,95))
        avg_uptime = float(np.mean(uptimes))
        breaches = len([l for l in latencies if l > threshold])

        result[r] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches
        }

    return result
