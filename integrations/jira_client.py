"""
Jira Integration for IT Support System

This module provides real Jira Cloud integration with demo fallback.
If Jira auth fails, it falls back to demo mode automatically.
"""

import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from typing import Optional, Dict, List
import random

# Configuration - will be loaded from Streamlit secrets or env
JIRA_DOMAIN = os.environ.get("JIRA_DOMAIN", "")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")

# Demo mode storage
DEMO_TICKETS = {}

class JiraClient:
    """
    Jira Cloud REST API client with demo fallback.
    """
    
    def __init__(self, domain: str = None, email: str = None, api_token: str = None):
        self.domain = domain or JIRA_DOMAIN
        self.email = email or JIRA_EMAIL
        self.api_token = api_token or JIRA_API_TOKEN
        self.base_url = f"https://{self.domain}/rest/api/3" if self.domain else ""
        self.auth = HTTPBasicAuth(self.email, self.api_token) if self.email and self.api_token else None
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.demo_mode = False
        self._check_mode()
    
    def _check_mode(self):
        """Check if we can use real Jira or need demo mode"""
        if not self.domain or not self.api_token:
            print("[Jira] No credentials - using demo mode")
            self.demo_mode = True
            return
        
        # Try to connect
        result = self.test_connection()
        if not result.get("success"):
            print(f"[Jira] Auth failed - using demo mode: {result.get('error', 'Unknown')}")
            self.demo_mode = True
        else:
            print(f"[Jira] Connected as {result.get('user')}")
    
    def test_connection(self) -> Dict:
        """Test the Jira connection and return user info"""
        if not self.base_url or not self.auth:
            return {"success": False, "error": "No credentials configured"}
        
        try:
            response = requests.get(
                f"{self.base_url}/myself",
                headers=self.headers,
                auth=self.auth,
                timeout=5
            )
            if response.status_code == 200:
                user = response.json()
                return {
                    "success": True,
                    "user": user.get("displayName"),
                    "email": user.get("emailAddress")
                }
            else:
                return {"success": False, "error": f"Status {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_projects(self) -> List[Dict]:
        """Get available Jira projects"""
        if self.demo_mode:
            return [{"key": "IT", "name": "IT Support", "id": "demo-1"}]
        
        try:
            response = requests.get(
                f"{self.base_url}/project",
                headers=self.headers,
                auth=self.auth,
                timeout=5
            )
            if response.status_code == 200:
                return [{"key": p["key"], "name": p["name"], "id": p["id"]} for p in response.json()]
            return [{"key": "IT", "name": "IT Support (Default)", "id": "default"}]
        except:
            return [{"key": "IT", "name": "IT Support (Default)", "id": "default"}]
    
    def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Task",
        priority: str = "Medium",
        labels: List[str] = None
    ) -> Dict:
        """Create a Jira issue (real or demo)"""
        
        if self.demo_mode:
            # Create demo ticket
            ticket_id = f"{project_key}-{random.randint(100, 999)}"
            DEMO_TICKETS[ticket_id] = {
                "key": ticket_id,
                "summary": summary,
                "description": description,
                "status": "Open",
                "priority": priority,
                "created": datetime.now().isoformat(),
                "assignee": "IT Support Team"
            }
            return {
                "success": True,
                "key": ticket_id,
                "id": f"demo-{ticket_id}",
                "url": f"https://demo.atlassian.net/browse/{ticket_id}",
                "demo": True
            }
        
        # Real Jira
        priority_map = {"Low": "Low", "Medium": "Medium", "High": "High", 
                        "Critical": "Highest", "Critical (VIP)": "Highest"}
        
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": {
                    "type": "doc", "version": 1,
                    "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
                },
                "issuetype": {"name": issue_type},
                "priority": {"name": priority_map.get(priority, "Medium")}
            }
        }
        if labels:
            payload["fields"]["labels"] = labels
        
        try:
            response = requests.post(
                f"{self.base_url}/issue",
                json=payload,
                headers=self.headers,
                auth=self.auth,
                timeout=10
            )
            if response.status_code in [200, 201]:
                issue = response.json()
                return {
                    "success": True,
                    "key": issue["key"],
                    "id": issue["id"],
                    "url": f"https://{self.domain}/browse/{issue['key']}"
                }
            return {"success": False, "error": f"Status {response.status_code}: {response.text[:200]}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_issue(self, issue_key: str) -> Dict:
        """Get issue details"""
        if self.demo_mode:
            if issue_key in DEMO_TICKETS:
                ticket = DEMO_TICKETS[issue_key]
                return {"success": True, **ticket, "url": f"https://demo.atlassian.net/browse/{issue_key}"}
            return {"success": False, "error": "Ticket not found"}
        
        try:
            response = requests.get(
                f"{self.base_url}/issue/{issue_key}",
                headers=self.headers,
                auth=self.auth,
                timeout=5
            )
            if response.status_code == 200:
                issue = response.json()
                fields = issue.get("fields", {})
                return {
                    "success": True,
                    "key": issue["key"],
                    "summary": fields.get("summary"),
                    "status": fields.get("status", {}).get("name"),
                    "priority": fields.get("priority", {}).get("name"),
                    "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else "Unassigned",
                    "url": f"https://{self.domain}/browse/{issue['key']}"
                }
            return {"success": False, "error": "Issue not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Singleton
_jira_client = None

def get_jira_client() -> JiraClient:
    """Get the Jira client singleton"""
    global _jira_client
    if _jira_client is None:
        _jira_client = JiraClient()
    return _jira_client

def reset_jira_client():
    """Reset the client (for credential changes)"""
    global _jira_client
    _jira_client = None


# Helper functions for agents
def jira_create_ticket(summary: str, description: str, priority: str = "Medium") -> str:
    """Create a ticket and return formatted result"""
    client = get_jira_client()
    projects = client.get_projects()
    project_key = projects[0]["key"] if projects else "IT"
    
    result = client.create_issue(
        project_key=project_key,
        summary=summary,
        description=description,
        priority=priority,
        labels=["ai-support", "it-support-genius"]
    )
    
    if result["success"]:
        demo_tag = " (Demo)" if result.get("demo") else ""
        return f"✅ Created [{result['key']}]({result['url']}){demo_tag}"
    return f"❌ Error: {result.get('error', 'Unknown')}"


def jira_get_ticket(ticket_key: str) -> str:
    """Get ticket info"""
    client = get_jira_client()
    result = client.get_issue(ticket_key)
    
    if result["success"]:
        return (
            f"**{result['key']}**: {result.get('summary', 'N/A')}\n"
            f"Status: {result.get('status', 'N/A')} | Priority: {result.get('priority', 'N/A')}\n"
            f"URL: {result.get('url', 'N/A')}"
        )
    return f"Error: {result.get('error', 'Unknown')}"


def is_demo_mode() -> bool:
    """Check if running in demo mode"""
    return get_jira_client().demo_mode


if __name__ == "__main__":
    print("Testing Jira Integration...")
    client = JiraClient()
    print(f"Mode: {'Demo' if client.demo_mode else 'Live'}")
    
    # Test create
    result = jira_create_ticket(
        summary="[Test] IT Support Genius",
        description="Test ticket from AI system",
        priority="Medium"
    )
    print(f"Create: {result}")
