# HirePilot AI REST API Specification

Base URL: `/api/v1`

## Key Resource Endpoints
- `/auth`: Authentication, JWT issuance, refresh tokens, user profile.
- `/jobs`: Job requisition lifecycle (Draft, Pending Approval, Published, Closed).
- `/candidates`: Candidate talent pool and profile details.
- `/applications`: Candidate job applications and recruitment pipeline stages.
- `/resumes`: Resume document uploads, parsing, and deterministic screening.
- `/interviews`: Scheduling, slot resolution, candidate interview records.
- `/approvals`: Human-in-the-loop approval workflows for critical HR actions.
- `/assistant`: Multi-agent conversation threads and streaming dispatch.
- `/analytics`: Real-time hiring funnel, conversion rates, and recruitment metrics.
- `/health`, `/ready`: Platform health and readiness probes.
