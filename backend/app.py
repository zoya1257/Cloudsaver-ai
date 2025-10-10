from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------------------------
# Initialize FastAPI app
# -------------------------------------------------
app = FastAPI()

# -------------------------------------------------
# ✅ CORS Configuration for GitHub Codespaces
# -------------------------------------------------
# IMPORTANT: Remove the trailing slash (/) in the URL
# Use your actual frontend Codespace URL below
origins = [
    "https://automatic-dollop-jjgpw4v79vxxc5grq-5173.app.github.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Allow only your frontend origin for safety
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Request Model
# -------------------------------------------------
class CostRequest(BaseModel):
    service: str
    usage_hours: int
    region: str

# -------------------------------------------------
# Root Endpoint (Test)
# -------------------------------------------------
@app.get("/")
def root():
    return {"message": "Backend is running correctly!"}

# -------------------------------------------------
# POST Endpoint: Cost Estimation
# -------------------------------------------------
@app.post("/api/estimate")
def estimate_cost(request: CostRequest):
    # Dummy AWS-like pricing rates
    rates = {
        "ec2": 0.12,
        "s3": 0.023,
        "lambda": 0.00001667
    }

    # Determine rate based on service (default = 0.10)
    rate = rates.get(request.service.lower(), 0.10)
    cost = request.usage_hours * rate

    # Return full structured response
    return {
        "service": request.service,
        "region": request.region,
        "estimated_cost": f"{cost:.2f}",
        "currency": "USD",
        "suggestions": [
            "Use AWS Free Tier if eligible.",
            f"Consider using spot instances for {request.service}.",
            "Monitor cost with AWS Cost Explorer."
        ]
    }

# -------------------------------------------------
# Run Command (for reference)
# -------------------------------------------------
# uvicorn app:app --host 0.0.0.0 --port 8001