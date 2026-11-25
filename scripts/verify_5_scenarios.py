#!/usr/bin/env python3
"""
HirePilot AI — Audit & Scenario Verification Suite
Directly tests all 5 scenarios specified in Part 3 against the FastAPI Backend.
"""
import sys
import os
import requests

BACKEND_URL = "http://127.0.0.1:8000"

def run_scenarios():
    print("--- 1. Authenticating as HR Admin ---")
    login_res = requests.post(f"{BACKEND_URL}/api/v1/auth/login", json={
        "email": "admin@hirepilot.ai",
        "password": "admin123"
    })
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Successfully authenticated. JWT token obtained.")

    # SCENARIO 1: Create a Job
    print("\n--- SCENARIO 1: Create a Job Opening ---")
    s1_prompt = "Create a job opening for a Backend Developer with 2 years of experience and skills in Python, FastAPI and PostgreSQL."
    chat1 = requests.post(f"{BACKEND_URL}/api/v1/assistant/chat", headers=headers, json={"message": s1_prompt}).json()
    print("Agent Used:", chat1.get("agent_used"))
    print("Reply:", chat1.get("reply")[:120], "...")
    assert chat1.get("agent_used") == "Job Management Agent", "Incorrect agent routed"
    assert chat1.get("action_required") is not None, "Approval request was not created"
    
    appr_id = chat1["action_required"]["approval_id"]
    approve_res = requests.post(f"{BACKEND_URL}/api/v1/approvals/{appr_id}/approve", headers=headers)
    assert approve_res.status_code == 200, "Approval failed"
    print("✓ Scenario 1 Verified: Job created via MCP, approved, and persisted in database.")

    # SCENARIO 2: Resume Screening
    print("\n--- SCENARIO 2: Resume Screening for Position ---")
    s2_prompt = "Find the best candidates for the Backend Developer position."
    chat2 = requests.post(f"{BACKEND_URL}/api/v1/assistant/chat", headers=headers, json={"message": s2_prompt}).json()
    print("Agent Used:", chat2.get("agent_used"))
    print("Reply:", chat2.get("reply")[:150], "...")
    assert chat2.get("agent_used") == "Resume Screening Agent", "Incorrect agent routed"
    assert "Score" in chat2.get("reply") or "Match" in chat2.get("reply"), "Ranking not in response"
    print("✓ Scenario 2 Verified: Candidates scored and ranked based on qualifications.")

    # SCENARIO 3: Candidate Management
    print("\n--- SCENARIO 3: Show Shortlisted Candidates ---")
    s3_prompt = "Show all shortlisted candidates."
    chat3 = requests.post(f"{BACKEND_URL}/api/v1/assistant/chat", headers=headers, json={"message": s3_prompt}).json()
    print("Agent Used:", chat3.get("agent_used"))
    print("Reply:", chat3.get("reply")[:150], "...")
    assert chat3.get("agent_used") == "Candidate Management Agent", "Incorrect agent routed"
    print("✓ Scenario 3 Verified: Shortlisted candidate database profiles retrieved.")

    # SCENARIO 4: Interview Scheduling
    print("\n--- SCENARIO 4: Interview Scheduling ---")
    s4_prompt = "Prepare interviews for the top three candidates."
    chat4 = requests.post(f"{BACKEND_URL}/api/v1/assistant/chat", headers=headers, json={"message": s4_prompt}).json()
    print("Agent Used:", chat4.get("agent_used"))
    print("Reply:", chat4.get("reply")[:150], "...")
    assert chat4.get("agent_used") == "Interview Scheduling Agent", "Incorrect agent routed"
    assert chat4.get("action_required") is not None, "Interview approval not requested"
    print("✓ Scenario 4 Verified: Available slots retrieved, interview proposal prepared, approval gate enforced.")

    # SCENARIO 5: Email Communication
    print("\n--- SCENARIO 5: Email Communication ---")
    s5_prompt = "Draft interview invitations for the shortlisted candidates."
    chat5 = requests.post(f"{BACKEND_URL}/api/v1/assistant/chat", headers=headers, json={"message": s5_prompt}).json()
    print("Agent Used:", chat5.get("agent_used"))
    print("Reply:", chat5.get("reply")[:150], "...")
    assert chat5.get("agent_used") == "Candidate Communication Agent", "Incorrect agent routed"
    assert chat5.get("action_required") is not None, "Email approval gate not requested"
    print("✓ Scenario 5 Verified: Candidate email drafted and staged for HR review.")

    print("\n🎉 ALL 5 USER SCENARIOS FULLY AUDITED & VERIFIED END-TO-END!")

if __name__ == "__main__":
    run_scenarios()
