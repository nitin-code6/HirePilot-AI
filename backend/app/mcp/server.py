import asyncio
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
from app.mcp.tools import MCPToolsRegistry

# Initialize FastMCP Server according to official Python MCP SDK
mcp_server = FastMCP("HirePilot Recruitment Server")

@mcp_server.tool()
def create_job(title: str, description: str, department: str = "Engineering", requirements: List[str] = None, location: str = "Remote") -> Dict[str, Any]:
    """Create a new job in HirePilot"""
    return MCPToolsRegistry.create_job(title, description, department, requirements, location)

@mcp_server.tool()
def list_jobs(status: str = None) -> List[Dict[str, Any]]:
    """List jobs filtered by status"""
    return MCPToolsRegistry.list_jobs(status)

@mcp_server.tool()
def get_job_details(job_id: str) -> Dict[str, Any]:
    """Get full requisition details for a specific job"""
    return MCPToolsRegistry.get_job_details(job_id)

@mcp_server.tool()
def list_candidates(search: str = None) -> List[Dict[str, Any]]:
    """Search and list candidate talent profiles"""
    return MCPToolsRegistry.list_candidates(search)

@mcp_server.tool()
def screen_candidate(resume_id: str, job_id: str) -> Dict[str, Any]:
    """Run deterministic resume screening against a job requisition"""
    return MCPToolsRegistry.screen_candidate(resume_id, job_id)

@mcp_server.tool()
def get_available_slots(interviewer_id: str = None) -> List[Dict[str, str]]:
    """Retrieve available interview slots"""
    return MCPToolsRegistry.get_available_slots(interviewer_id)

@mcp_server.tool()
def draft_email(recipient_email: str, candidate_name: str, job_title: str, template_type: str = "interview_invite") -> Dict[str, str]:
    """Draft a candidate email template"""
    return MCPToolsRegistry.draft_email(recipient_email, candidate_name, job_title, template_type)

@mcp_server.tool()
def get_hiring_statistics() -> Dict[str, Any]:
    """Get real-time recruitment platform statistics"""
    return MCPToolsRegistry.get_hiring_statistics()

if __name__ == "__main__":
    mcp_server.run()
