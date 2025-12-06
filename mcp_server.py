"""
MCP Server for IT Support System

This module demonstrates Model Context Protocol (MCP) integration,
showing how standardized tool access works compared to traditional APIs.

Run with: python mcp_server.py
"""

from typing import Any
import json
import random
from datetime import datetime, timedelta

# Simulated databases
USERS_DB = {
    "user123": {"name": "John Smith", "department": "Engineering", "vip": False, "location": "NYC"},
    "user_ceo": {"name": "Jane Doe", "department": "Executive", "vip": True, "location": "SF"},
    "user_dev": {"name": "Bob Developer", "department": "Engineering", "vip": False, "location": "NYC"},
}

TICKETS_DB = {
    "INC-12345": {"status": "Open", "priority": "High", "assignee": "IT-Team-A", "created": "2025-12-05"},
    "INC-12346": {"status": "Resolved", "priority": "Medium", "assignee": "IT-Team-B", "created": "2025-12-04"},
}

SYSTEMS_DB = {
    "vpn-gateway-1": {"status": "healthy", "uptime": "99.9%", "region": "us-east"},
    "mail-server-1": {"status": "degraded", "uptime": "98.5%", "region": "us-west"},
    "ad-controller-1": {"status": "healthy", "uptime": "99.99%", "region": "us-east"},
}


class MCPServer:
    """
    Model Context Protocol Server
    
    This server exposes IT support tools in a standardized way that any
    MCP-compatible client can consume. This demonstrates the power of MCP
    for enterprise tool integration.
    """
    
    def __init__(self):
        self.tools = {
            "get_user_info": self.get_user_info,
            "get_ticket_status": self.get_ticket_status,
            "create_ticket": self.create_ticket,
            "check_system_health": self.check_system_health,
            "reset_password": self.reset_password,
            "unlock_account": self.unlock_account,
        }
        
    def list_tools(self) -> list:
        """Return list of available tools (MCP discovery)"""
        return [
            {
                "name": "get_user_info",
                "description": "Retrieve user profile information from HR/IT systems",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID to look up"}
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "get_ticket_status",
                "description": "Get the status of a ServiceNow/Jira ticket",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {"type": "string", "description": "Ticket ID (e.g., INC-12345)"}
                    },
                    "required": ["ticket_id"]
                }
            },
            {
                "name": "create_ticket",
                "description": "Create a new IT support ticket",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "priority": {"type": "string", "enum": ["Low", "Medium", "High", "Critical"]},
                        "requester": {"type": "string"}
                    },
                    "required": ["title", "description", "priority", "requester"]
                }
            },
            {
                "name": "check_system_health",
                "description": "Check health status of IT infrastructure systems",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "system_id": {"type": "string", "description": "System identifier"}
                    },
                    "required": ["system_id"]
                }
            },
            {
                "name": "reset_password",
                "description": "Initiate password reset for a user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"}
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "unlock_account",
                "description": "Unlock a locked user account",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"}
                    },
                    "required": ["user_id"]
                }
            }
        ]
    
    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Execute a tool call (MCP standard method)"""
        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            result = self.tools[tool_name](**arguments)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Tool implementations
    def get_user_info(self, user_id: str) -> dict:
        """Retrieve user information from HR/IT database"""
        if user_id in USERS_DB:
            return USERS_DB[user_id]
        return {"error": "User not found", "user_id": user_id}
    
    def get_ticket_status(self, ticket_id: str) -> dict:
        """Get ticket status from ServiceNow/Jira"""
        if ticket_id in TICKETS_DB:
            return TICKETS_DB[ticket_id]
        return {"error": "Ticket not found", "ticket_id": ticket_id}
    
    def create_ticket(self, title: str, description: str, priority: str, requester: str) -> dict:
        """Create a new incident ticket"""
        ticket_id = f"INC-{random.randint(10000, 99999)}"
        TICKETS_DB[ticket_id] = {
            "status": "New",
            "priority": priority,
            "assignee": "Unassigned",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "title": title,
            "requester": requester
        }
        return {
            "ticket_id": ticket_id,
            "message": f"Ticket {ticket_id} created successfully",
            "eta": "Response within 4 hours" if priority in ["High", "Critical"] else "Response within 24 hours"
        }
    
    def check_system_health(self, system_id: str) -> dict:
        """Check system health status"""
        if system_id in SYSTEMS_DB:
            return SYSTEMS_DB[system_id]
        # Return generic healthy status for unknown systems
        return {"status": "unknown", "message": f"No monitoring data for {system_id}"}
    
    def reset_password(self, user_id: str) -> dict:
        """Initiate password reset"""
        if user_id in USERS_DB:
            reset_link = f"https://id.company.com/reset/{random.randint(100000, 999999)}"
            return {
                "success": True,
                "message": f"Password reset initiated for {user_id}",
                "reset_link": reset_link,
                "expires": (datetime.now() + timedelta(hours=24)).isoformat()
            }
        return {"success": False, "error": "User not found"}
    
    def unlock_account(self, user_id: str) -> dict:
        """Unlock a user account"""
        if user_id in USERS_DB:
            return {
                "success": True,
                "message": f"Account {user_id} has been unlocked",
                "note": "User should be able to login immediately"
            }
        return {"success": False, "error": "User not found"}


# Demo: Show MCP server capabilities
if __name__ == "__main__":
    print("=" * 60)
    print("🔌 MCP Server for IT Support")
    print("=" * 60)
    
    server = MCPServer()
    
    # 1. List available tools (MCP Discovery)
    print("\n📋 Available Tools (MCP Discovery):")
    print("-" * 40)
    for tool in server.list_tools():
        print(f"  • {tool['name']}: {tool['description']}")
    
    # 2. Demo tool calls
    print("\n🔧 Demo Tool Calls:")
    print("-" * 40)
    
    # Get user info
    result = server.call_tool("get_user_info", {"user_id": "user_ceo"})
    print(f"\n1. get_user_info('user_ceo'):")
    print(f"   {json.dumps(result, indent=2)}")
    
    # Check ticket status
    result = server.call_tool("get_ticket_status", {"ticket_id": "INC-12345"})
    print(f"\n2. get_ticket_status('INC-12345'):")
    print(f"   {json.dumps(result, indent=2)}")
    
    # Create new ticket
    result = server.call_tool("create_ticket", {
        "title": "VPN Connection Issues",
        "description": "Unable to connect to corporate VPN",
        "priority": "High",
        "requester": "user123"
    })
    print(f"\n3. create_ticket(...):")
    print(f"   {json.dumps(result, indent=2)}")
    
    # Check system health
    result = server.call_tool("check_system_health", {"system_id": "vpn-gateway-1"})
    print(f"\n4. check_system_health('vpn-gateway-1'):")
    print(f"   {json.dumps(result, indent=2)}")
    
    print("\n" + "=" * 60)
    print("✅ MCP Server Demo Complete")
    print("=" * 60)
