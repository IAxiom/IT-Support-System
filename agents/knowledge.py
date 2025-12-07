"""
Knowledge Agent with Inline Knowledge Base

Uses a simple in-memory knowledge base for demo reliability,
with optional RAG enhancement when embeddings are available.
"""

from state import AgentState, AuditLogger
from utils.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# In-memory knowledge base for demo reliability
KNOWLEDGE_BASE = {
    "password": {
        "policy": "Password Policy: Minimum 12 characters, must include uppercase, lowercase, number, and special character. Passwords expire every 90 days. No reuse of last 10 passwords.",
        "reset": "To reset your password: Visit id.company.com/reset, enter your email, and follow the link. If you don't receive it, check spam or contact IT at (555) 123-4567."
    },
    "wifi": {
        "guest": "Guest WiFi Password: 'Innovation2025!' - This rotates every Monday. Connect to 'Company-Guest' network.",
        "corporate": "Corporate WiFi: Connect to 'Company-Secure' using your domain credentials. This provides full internal access.",
        "troubleshooting": "WiFi Troubleshooting: 1) Restart WiFi on device, 2) Forget network and reconnect, 3) Move closer to access point, 4) Restart device, 5) Contact IT if issue persists."
    },
    "vpn": {
        "setup": "VPN Setup: Download GlobalProtect from software.company.com, install, and connect using your domain credentials.",
        "troubleshooting": "VPN Issues: 1) Ensure latest VPN client, 2) Restart home router, 3) Try Ethernet instead of WiFi, 4) Try alternate gateway, 5) Contact IT if repeated failures."
    },
    "expense": {
        "policy": "Expense Policy: Client dinners capped at $75/person. Alcohol only with VP approval. Submit via Concur within 30 days.",
        "submit": "To submit expenses: Open Concur, create new report, attach receipts, select appropriate category, submit for manager approval."
    },
    "mfa": {
        "reset": "MFA Reset: Visit id.company.com/reset to reset your authenticator. You'll need backup codes or contact IT with ID verification.",
        "setup": "MFA Setup: Download Microsoft Authenticator or Google Authenticator, scan QR code from id.company.com/enroll."
    },
    "laptop": {
        "refresh": "Laptop Refresh: Engineering gets MacBook Pro every 3 years, Sales gets MacBook Air every 3 years. Early refresh requires VP approval.",
        "support": "Laptop Issues: Submit ticket at helpdesk.company.com or call (555) 123-4567. Include your asset tag (on bottom of laptop)."
    },
    "onboarding": {
        "new_hire": "New Hire Onboarding: Manager submits form in Workday 3 days before start. IT provisions email, Slack, laptop, and badge access.",
        "first_day": "First Day: Pick up laptop from IT (Building A, Room 101), complete security training, set up MFA."
    },
    "it_contact": {
        "support": "IT Support: Phone (555) 123-4567, Email support@company.com, Portal helpdesk.company.com. Hours: M-F 8AM-6PM, Emergency after-hours available."
    }
}


class KnowledgeAgent:
    def __init__(self):
        pass

    def _search_knowledge(self, query: str) -> str:
        """Search the in-memory knowledge base"""
        query_lower = query.lower()
        matches = []
        
        # Search through all categories and topics
        for category, topics in KNOWLEDGE_BASE.items():
            if category in query_lower:
                for topic, content in topics.items():
                    matches.append(content)
                    if len(matches) >= 3:
                        break
        
        # If no category match, search content
        if not matches:
            for category, topics in KNOWLEDGE_BASE.items():
                for topic, content in topics.items():
                    if any(word in query_lower for word in topic.split("_")):
                        matches.append(content)
                    elif any(word in content.lower() for word in query_lower.split()[:3]):
                        matches.append(content)
                    if len(matches) >= 3:
                        break
        
        return "\n\n".join(matches[:3]) if matches else ""

    def run(self, state: AgentState):
        print("--- Knowledge Agent ---")
        messages = state['messages']
        last_message = messages[-1]['content']
        
        # Search knowledge base
        context = self._search_knowledge(last_message)
        docs_found = len(context.split("\n\n")) if context else 0
        
        # Generate response (works with or without LLM)
        if context:
            confidence = 0.85
            response = f"Based on our IT documentation:\n\n{context}"
        else:
            response = "I don't have specific information about this in our knowledge base. Let me connect you with our IT team.\n\n📞 **IT Support:** (555) 123-4567\n📧 **Email:** support@company.com"
            confidence = 0.3
        
        # Add confidence (single, clean indicator)
        emoji = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.4 else "🔴"
        response = f"{response}\n\n{emoji} *Confidence: {confidence:.0%}*"
        
        # Log the action
        audit_log = AuditLogger.log(state, "KnowledgeAgent", "knowledge_query", {
            "query": last_message[:50],
            "docs_found": docs_found,
            "confidence": confidence
        })
        
        return {
            "messages": [{"role": "assistant", "content": response}],
            "next_agent": "END",
            "confidence": confidence,
            "audit_log": audit_log
        }
