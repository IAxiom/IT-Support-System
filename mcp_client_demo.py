"""
MCP Client Demo for IT Support System

This demonstrates how an MCP client (like VS Code, Claude Desktop, or custom apps)
connects to and uses MCP servers for standardized tool access.

This shows the difference between:
- Traditional API: Each integration needs custom code
- MCP: Standardized protocol, tool discovery, and execution
"""

from mcp_server import MCPServer
import json


def demo_mcp_vs_traditional():
    """
    Demonstrate how MCP simplifies tool integration compared to traditional APIs
    """
    
    print("=" * 70)
    print("🔄 MCP vs Traditional API Integration Demo")
    print("=" * 70)
    
    # Traditional API approach (what we DON'T want)
    print("\n❌ TRADITIONAL APPROACH (Before MCP):")
    print("-" * 50)
    print("""
    # Each system needs custom integration code:
    
    # Jira Integration
    from jira import JIRA
    jira = JIRA(server='https://company.atlassian.net', token='...')
    ticket = jira.create_issue(project='IT', summary='...')
    
    # ServiceNow Integration  
    import servicenow
    sn = servicenow.Client('https://company.service-now.com', user='...')
    incident = sn.incidents.create(short_description='...')
    
    # Active Directory Integration
    import ldap
    conn = ldap.initialize('ldap://ad.company.com')
    conn.simple_bind_s('admin@company.com', '...')
    conn.modify_s('cn=user,dc=company,dc=com', [(ldap.MOD_REPLACE, 'locked', 'false')])
    
    # Different APIs, different authentication, different error handling!
    """)
    
    # MCP approach (what we DO want)
    print("\n✅ MCP APPROACH (Standardized):")
    print("-" * 50)
    
    # Initialize MCP client connecting to our server
    client = MCPClient()
    
    # 1. Discover available tools (standardized)
    print("\n1️⃣ Tool Discovery (One API for all systems):")
    tools = client.discover_tools()
    for tool in tools[:3]:  # Show first 3
        print(f"   • {tool['name']}")
    print(f"   ... and {len(tools) - 3} more tools")
    
    # 2. Execute tools (standardized interface)
    print("\n2️⃣ Tool Execution (Same pattern for everything):")
    
    # Same interface regardless of underlying system
    examples = [
        ("get_user_info", {"user_id": "user_ceo"}, "HR/AD System"),
        ("get_ticket_status", {"ticket_id": "INC-12345"}, "ServiceNow/Jira"),
        ("check_system_health", {"system_id": "vpn-gateway-1"}, "Monitoring"),
    ]
    
    for tool_name, args, system in examples:
        result = client.call_tool(tool_name, args)
        status = "✓" if result.get("success") else "✗"
        print(f"\n   {status} {tool_name} ({system}):")
        print(f"      Input: {args}")
        print(f"      Result: {json.dumps(result.get('result', result.get('error')), indent=2)[:100]}...")
    
    # 3. Show the key benefits
    print("\n" + "=" * 70)
    print("🎯 KEY MCP BENEFITS:")
    print("=" * 70)
    print("""
    1. STANDARDIZED DISCOVERY
       → Any MCP client can discover available tools automatically
       → No hardcoded integrations needed
    
    2. UNIFORM INTERFACE  
       → Same call_tool() pattern for ALL systems
       → Same JSON schema for inputs/outputs
    
    3. SECURITY & GOVERNANCE
       → Centralized access control
       → Audit logging in one place
       → No credentials scattered in code
    
    4. COMPOSABILITY
       → Tools from different servers can work together
       → AI agents can discover and use tools dynamically
    
    5. ENTERPRISE READY
       → Works with VS Code, Claude Desktop, custom apps
       → Scales from prototype to production
    """)


class MCPClient:
    """
    Simulated MCP Client
    
    In production, this would use the official MCP SDK and connect
    to servers via stdio, HTTP, or WebSocket transports.
    """
    
    def __init__(self):
        # Connect to our MCP server
        self.server = MCPServer()
        print("   🔌 MCP Client initialized")
        print("   📡 Connected to: IT Support MCP Server")
    
    def discover_tools(self) -> list:
        """Discover available tools from the server"""
        return self.server.list_tools()
    
    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Call a tool on the server"""
        return self.server.call_tool(tool_name, arguments)


def demo_agent_integration():
    """
    Show how an AI agent uses MCP to access tools
    """
    print("\n" + "=" * 70)
    print("🤖 AI Agent + MCP Integration Demo")
    print("=" * 70)
    
    print("""
    When a user asks: "My VPN isn't working and I need help"
    
    The AI agent can:
    
    1. DISCOVER what tools are available:
       → Finds: check_system_health, get_user_info, create_ticket...
    
    2. PLAN which tools to use:
       → "I'll check VPN health, then user status, then create ticket if needed"
    
    3. EXECUTE tools via MCP:
       → call_tool("check_system_health", {"system_id": "vpn-gateway-1"})
       → call_tool("get_user_info", {"user_id": "current_user"})
       → call_tool("create_ticket", {...})
    
    4. RESPOND with results:
       → "I checked the VPN gateway - it's healthy. I've created ticket 
          INC-54321 to investigate your connection specifically."
    
    This is EXACTLY what our IT Support System does!
    """)
    
    # Live demo
    print("\n🔴 LIVE DEMO:")
    print("-" * 50)
    
    client = MCPClient()
    
    # Simulate agent workflow
    print("\n   Agent: Checking VPN gateway health...")
    result = client.call_tool("check_system_health", {"system_id": "vpn-gateway-1"})
    print(f"   Result: {result['result']}")
    
    print("\n   Agent: VPN is healthy, creating support ticket...")
    result = client.call_tool("create_ticket", {
        "title": "User VPN Connection Issue",
        "description": "User unable to connect despite healthy gateway. Needs investigation.",
        "priority": "Medium",
        "requester": "user123"
    })
    print(f"   Result: Ticket {result['result']['ticket_id']} created!")
    
    print("\n   Agent: 'I've created ticket {ticket_id}. Our team will investigate within 24 hours.'")


if __name__ == "__main__":
    demo_mcp_vs_traditional()
    demo_agent_integration()
    
    print("\n" + "=" * 70)
    print("✅ MCP Demo Complete!")
    print("=" * 70)
    print("\nTo run: python mcp_client_demo.py")
