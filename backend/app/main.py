from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.database.session import engine, Base
from app.api.v1 import auth, jobs, candidates, resumes, approvals, assistant, interviews, analytics

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description="HirePilot AI - Autonomous AI Recruitment Management Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 Routers
api_v1_prefix = "/api/v1"
app.include_router(auth.router, prefix=api_v1_prefix)
app.include_router(jobs.router, prefix=api_v1_prefix)
app.include_router(candidates.router, prefix=api_v1_prefix)
app.include_router(resumes.router, prefix=api_v1_prefix)
app.include_router(approvals.router, prefix=api_v1_prefix)
app.include_router(assistant.router, prefix=api_v1_prefix)
app.include_router(interviews.router, prefix=api_v1_prefix)
app.include_router(analytics.router, prefix=api_v1_prefix)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "service": "HirePilot AI Backend"}

@app.get("/ready", tags=["System"])
def readiness_check():
    return {"status": "ready", "database": "connected"}

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
