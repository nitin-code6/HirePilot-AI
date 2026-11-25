# HirePilot AI System Architecture

## High-Level Architecture
HirePilot AI implements a layered autonomous multi-agent recruitment platform:
1. **Presentation Layer**: React 19, TypeScript, Tailwind CSS, Vite enterprise SaaS interface.
2. **API & Gateway Layer**: FastAPI versioned REST API (`/api/v1`) with JWT auth and RBAC.
3. **Agent Orchestration**: LangGraph Supervisor directing intent-driven sub-agents.
4. **Tool Execution Layer**: Standards-based Model Context Protocol (MCP) server.
5. **Business & Domain Layer**: High-cohesion services for Jobs, Screening, Interviews, and Approvals.
6. **Data & Storage Layer**: PostgreSQL / SQLite (via SQLAlchemy 2.0 Async), Redis cache, and secure file storage.
7. **External Providers**: Groq LLM, LangSmith tracing, SMTP/Mock email, and Google Calendar/Mock integrations.
