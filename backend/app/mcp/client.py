import asyncio
from typing import Dict, Any
from app.mcp.tools import MCPToolsRegistry

class MCPClientIntegration:
    """
    Standard MCP Client that connects agents to the Model Context Protocol tools.
    """
    @staticmethod
    async def call_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        registry_methods = {
            "create_job": MCPToolsRegistry.create_job,
            "list_jobs": MCPToolsRegistry.list_jobs,
            "get_job_details": MCPToolsRegistry.get_job_details,
            "list_candidates": MCPToolsRegistry.list_candidates,
            "screen_candidate": MCPToolsRegistry.screen_candidate,
            "get_available_slots": MCPToolsRegistry.get_available_slots,
            "draft_email": MCPToolsRegistry.draft_email,
            "get_hiring_statistics": MCPToolsRegistry.get_hiring_statistics
        }
        
        func = registry_methods.get(tool_name)
        if not func:
            return {"error": f"Tool '{tool_name}' not found on MCP Server"}
            
        # Execute tool
        try:
            return func(**arguments)
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}

mcp_client = MCPClientIntegration()
