#!/bin/bash
# HirePilot AI Health Check Script

BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"

echo "Checking HirePilot AI Backend Health at $BACKEND_URL/health..."
HEALTH=$(curl -s "$BACKEND_URL/health")
echo "Response: $HEALTH"

echo "Checking Readiness at $BACKEND_URL/ready..."
READY=$(curl -s "$BACKEND_URL/ready")
echo "Response: $READY"

if [[ "$HEALTH" == *"healthy"* ]]; then
  echo "Backend is HEALTHY."
  exit 0
else
  echo "Backend health check FAILED."
  exit 1
fi
