from pydantic import BaseModel, Field
from typing import List, Optional

class MCPCreateJobInput(BaseModel):
    title: str = Field(..., description="Job requisition title")
    description: str = Field(..., description="Full job description")
    department: str = Field("Engineering", description="Department name")
    requirements: List[str] = Field(default_factory=list, description="List of required skills")
    location: str = Field("Remote", description="Job location")

class MCPScreenCandidateInput(BaseModel):
    resume_id: str = Field(..., description="ID of the uploaded resume document")
    job_id: str = Field(..., description="ID of the requisition to screen against")
