import asyncio
from typing import Dict, Any, List
from app.mcp.tools import MCPToolsRegistry

class MCPClientIntegration:
    """
    Standard MCP Client that connects LangGraph agents to the Model Context Protocol tools.
    Supports both async and synchronous execution against the MCP Server tools.
    """
    @staticmethod
    def call_tool_sync(tool_name: str, arguments: Dict[str, Any] = None) -> Any:
        args = arguments or {}
        registry_methods = {
            "create_job": MCPToolsRegistry.create_job,
            "list_jobs": MCPToolsRegistry.list_jobs,
            "get_job_details": MCPToolsRegistry.get_job_details,
            "update_job": MCPToolsRegistry.update_job,
            "close_job": MCPToolsRegistry.close_job,
            "create_candidate": MCPToolsRegistry.create_candidate,
            "list_candidates": MCPToolsRegistry.list_candidates,
            "get_candidate_details": MCPToolsRegistry.get_candidate_details,
            "update_application_status": MCPToolsRegistry.update_application_status,
            "screen_candidate": MCPToolsRegistry.screen_candidate,
            "get_screening_report": MCPToolsRegistry.get_screening_report,
            "get_available_slots": MCPToolsRegistry.get_available_slots,
            "schedule_interview": MCPToolsRegistry.schedule_interview,
            "draft_email": MCPToolsRegistry.draft_email,
            "get_hiring_statistics": MCPToolsRegistry.get_hiring_statistics
        }
        
        func = registry_methods.get(tool_name)
        if not func:
            return {"error": f"Tool '{tool_name}' not found on MCP Server"}
            
        try:
            return func(**args)
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}

    @classmethod
    async def call_tool(cls, tool_name: str, arguments: Dict[str, Any] = None) -> Any:
        return cls.call_tool_sync(tool_name, arguments)

mcp_client = MCPClientIntegration()
