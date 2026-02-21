from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

with open("q-vercel-latency .json") as f:
    telemetry = json.load(f)

class Req(BaseModel):
    regions: List[str]
    threshold_ms: int

@app.post("/")
def check_latency(req: Req):
    res = {}

    for region in req.regions:
        data = [x for x in telemetry if x["region"] == region]

        lat = [d["latency_ms"] for d in data]
        up = [d["uptime"] for d in data]

        res[region] = {
            "avg_latency": float(np.mean(lat)),
            "p95_latency": float(np.percentile(lat,95)),
            "avg_uptime": float(np.mean(up)),
            "breaches": len([l for l in lat if l > req.threshold_ms])
        }

    return res