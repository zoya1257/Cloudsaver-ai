from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from typing import Optional

app = FastAPI(title="CloudSaver-AI (MVP)")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
PRICING_PATH = os.path.join(DATA_DIR, "pricing_defaults.json")
PROFILES_PATH = os.path.join(DATA_DIR, "profiles.json")

# Load static pricing & profiles
with open(PRICING_PATH, "r") as f:
    PRICING = json.load(f)
with open(PROFILES_PATH, "r") as f:
    PROFILES = json.load(f)

class EstimateRequest(BaseModel):
    region: str
    profile: str
    traffic: Optional[str] = None

@app.post("/api/estimate")
def estimate(payload: EstimateRequest):
    region = payload.region
    profile = payload.profile

    if region not in PRICING:
        raise HTTPException(status_code=400, detail=f"Region '{region}' not supported.")
    if profile not in PROFILES:
        raise HTTPException(status_code=400, detail=f"Profile '{profile}' not found.")

    region_prices = PRICING[region]
    profile_cfg = PROFILES[profile]
    components = []
    total_monthly = 0.0

    for comp in profile_cfg.get("components", []):
        service = comp["service"]
        units = comp.get("units", 1)
        billing = comp.get("billing", "monthly")

        if service not in region_prices:
            components.append({
                "service": service,
                "note": "Price not found for region"
            })
            continue

        price = float(region_prices[service])
        if billing == "hourly":
            monthly = price * 24 * 30 * units
            weekly = price * 24 * 7 * units
        else:
            monthly = price * units
            weekly = (price / 30.0) * 7.0 * units

        components.append({
            "service": service,
            "monthly": round(monthly, 4),
            "weekly": round(weekly, 4),
            "units": units
        })
        total_monthly += monthly

    return {
        "region": region,
        "profile": profile,
        "7d_estimate": round((total_monthly / 30.0) * 7.0, 4),
        "30d_estimate": round(total_monthly, 4),
        "components": components,
        "notes": "Approximate estimates — integrate AWS Pricing API for real data."
    }
