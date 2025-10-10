#!/bin/bash
cd backend && uvicorn app:app --reload --port 8001 &
cd frontend && npm run dev