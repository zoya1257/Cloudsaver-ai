CloudSaver-AI

AI-powered AWS Cost & Resource Optimization Assistant

CloudSaver-AI is an intelligent module that helps AWS users — from beginners to startups — estimate their 7-day and 30-day cloud costs, get personalized optimization suggestions, and understand which AWS services best fit their needs.
It works in two modes:

Account Scan Mode: Scans your AWS account (read-only) to analyze real usage and cost trends.

Estimator Mode: Lets you describe your workload in simple language, then predicts estimated cost, suggests services, and provides startup-friendly guidance.

🧭 Features

🔍 Real-time cost analysis for AWS infrastructure

🤖 AI-powered recommendations for cost optimization

🌍 Region-aware cost breakdown (supports AWS regions)

💬 Multi-language support (optional via AWS Translate / Google Translate)

🧩 Beginner-friendly suggestions — best starting point for small projects

📊 Simple dashboard UI (Streamlit / React)

📁 Repository Structure
cloudsaver-ai/
├─ README.md
├─ .env.example
├─ .gitignore
├─ backend/
│  ├─ app.py                 # FastAPI / Flask main backend app
│  ├─ requirements.txt
│  ├─ routes/
│  │  ├─ scan.py             # /api/scan - scans AWS account
│  │  ├─ estimate.py         # /api/estimate - cost estimator
│  │  └─ recommend.py        # /api/recommend - AI-based suggestions
│  ├─ services/
│  │  ├─ aws_client.py       # Boto3 client for AWS APIs
│  │  ├─ cost_estimator.py   # pricing logic / static table + AWS Pricing API
│  │  ├─ infra_infer.py      # infers resources from user input
│  │  └─ llm_agent.py        # connects with LLM (OpenAI or Bedrock)
│  ├─ utils/
│  │  ├─ validators.py
│  │  └─ serializers.py
│  └─ infra/
│     └─ read_only_iam.json  # IAM policy snippet for user setup
├─ frontend/
│  ├─ streamlit_app.py       # Streamlit UI for MVP
│  └─ react_app/             # Optional React frontend
├─ data/
│  ├─ pricing_defaults.json  # Cached base prices for AWS regions
│  └─ profiles.json          # Starter workload profiles
├─ docs/
│  └─ architecture.md
└─ tests/
   └─ test_estimator.py

⚙️ How It Works (Flow Overview)

User input (two modes):

Account Scan Mode: User provides a read-only IAM role → system scans usage and cost data.

Estimator Mode: User describes their workload (e.g., “host a small website”) or selects region + expected traffic.

Data collection:

Fetches usage metrics (via Cost Explorer, CloudWatch, etc.)

Or infers defaults from workload description (static profiles).

Cost calculation:

Uses AWS Pricing API or cached pricing_defaults.json

Calculates 7-day and 30-day cost ranges.

AI analysis & recommendations:

The LLM processes cost breakdowns and suggests optimization actions in plain language.

Example: “Stop idle EC2 instance i-xxxxxx” or “Use S3 Infrequent Access.”

Frontend output:

Visual breakdown, estimated costs, and top 3 cost-saving suggestions.

Optional “how to implement” with CLI commands or AWS Console paths.

🔌 API Endpoints (MVP)
POST /api/scan
Request: { "role_arn": "<read-only-role-arn>", "region": "us-east-1" }
Response:
{
  "summary": { "7d_estimate": 12.4, "30d_estimate": 52.3 },
  "breakdown": [{ "service": "EC2", "30d": 30.2 }, ...],
  "suggestions": ["Stop instance i-abc during off-hours", ...]
}

POST /api/estimate
Request: { "region": "ap-south-1", "profile": "small-web", "traffic": "200/day" }
Response:
{ "7d": 2.5, "30d": 10.0, "components": {...}, "how_to_start": "Use Lightsail $5 plan" }

POST /api/recommend
Request: { "context": {...}, "lang": "en" }
Response:
{ "text": "Your estimated monthly cost is $10. Use S3 Static Hosting.", "actions": [...] }

🔐 IAM Read-only Policy

Save this as backend/infra/read_only_iam.json and instruct users to attach it.

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ce:GetCostForecast",
        "ce:GetDimensionValues",
        "ec2:DescribeInstances",
        "s3:ListAllMyBuckets",
        "rds:DescribeDBInstances",
        "lambda:ListFunctions",
        "cloudwatch:GetMetricData",
        "cloudwatch:ListMetrics"
      ],
      "Resource": "*"
    }
  ]
}

🧾 Environment Variables

.env.example

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
OPENAI_API_KEY=
PRICING_CACHE_PATH=./data/pricing_defaults.json
LLM_PROVIDER=openai
PORT=8000

🧠 AI Prompt Template
System: You are CloudSaver AI. You receive cost breakdowns and resource data.
Generate:
1. A short summary of the cost in simple English.
2. Top 3 cost-saving actions with steps or AWS CLI commands.
3. Estimated 7-day and 30-day cost.

User data:
- region: {region}
- breakdown: {json_breakdown}
- profile: {profile}

🧪 Testing Criteria

/api/estimate returns numeric 7-day and 30-day estimates.

/api/scan returns at least one actionable suggestion.

LLM suggestions always include a concrete step (e.g., "stop instance").

UI displays charts, breakdown, and recommendations properly.

🗓️ Development Plan

Day 0 – Setup

Initialize repo, add README, and create folders.

Day 1 – Backend Core

Build /api/estimate using FastAPI + static pricing data.

Add estimator test.

Day 2 – AI Integration

Connect OpenAI / Bedrock for natural language suggestions.

Day 3 – Frontend (Streamlit MVP)

Build UI for inputs & outputs.

Show cost estimates and AI suggestions.

Day 4 – Polish & Submit

Optional: add account scan mode.

Record 2-min demo video for submission.
