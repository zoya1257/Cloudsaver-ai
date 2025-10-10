from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AWS AI Cost Estimator")

# ---------- Data Models ----------
class CostProfile(BaseModel):
    service: str
    usage_hours: float
    region: str

# ---------- Estimation Function ----------
def estimate_cost(service: str, usage_hours: float, region: str):
    base_rates = {
        "EC2": 0.12,
        "S3": 0.023,
        "Lambda": 0.0000167,
        "RDS": 0.25
    }

    region_modifier = {
        "us-east-1": 1.0,
        "us-west-1": 1.1,
        "ap-south-1": 0.9,
        "eu-central-1": 1.2
    }

    service_rate = base_rates.get(service, 0.1)
    region_factor = region_modifier.get(region, 1.0)

    estimated_cost = service_rate * usage_hours * region_factor
    return estimated_cost

# ---------- AI-Like Suggestion Logic ----------
def suggest_optimization(service: str, usage_hours: float, region: str):
    suggestions = []

    if service == "EC2":
        if usage_hours > 500:
            suggestions.append("Consider Reserved Instances or Savings Plans to reduce EC2 cost.")
        else:
            suggestions.append("Use Spot Instances for short workloads.")
    elif service == "S3":
        suggestions.append("Enable S3 Intelligent-Tiering for infrequent access data.")
    elif service == "Lambda":
        suggestions.append("Optimize function memory size for best cost-performance ratio.")
    elif service == "RDS":
        suggestions.append("Use Aurora Serverless if your DB workload is variable.")
    else:
        suggestions.append("Enable Cost Explorer to analyze detailed usage patterns.")

    if region != "us-east-1":
        suggestions.append("Consider deploying in us-east-1 region for lower base rates.")

    return suggestions

# ---------- API Endpoint ----------
@app.post("/api/estimate")
def get_estimate(profile: CostProfile):
    cost = estimate_cost(profile.service, profile.usage_hours, profile.region)
    suggestions = suggest_optimization(profile.service, profile.usage_hours, profile.region)
    return {
        "estimated_cost": round(cost, 2),
        "currency": "USD",
        "suggestions": suggestions
    }