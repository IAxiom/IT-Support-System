from state import AgentState, AuditLogger
from tools.mcp_tools import get_user_context
from datetime import datetime
import os

# Import Jira integration
try:
    from integrations.jira_client import jira_create_ticket, is_demo_mode
    JIRA_AVAILABLE = True
except ImportError:
    JIRA_AVAILABLE = False
    def jira_create_ticket(*args, **kwargs):
        return "Jira integration not available"
    def is_demo_mode():
        return True

class EscalationAgent:
    def __init__(self):
        self.workarounds = {
            "vpn": "💡 **While you wait:** 1) Restart VPN client, 2) Try different region, 3) Use mobile hotspot.",
            "email": "💡 **While you wait:** 1) Try webmail at mail.company.com, 2) Check spam folder.",
            "password": "💡 **While you wait:** 1) Try 'Forgot Password' link, 2) Check Caps Lock.",
            "slow": "💡 **While you wait:** 1) Close browser tabs, 2) Restart computer.",
            "wifi": "💡 **While you wait:** 1) Forget network and reconnect, 2) Move closer to access point."
        }
        
        self.resolution_times = {
            "Critical (VIP)": 15, "High": 30, "Medium": 60, "Low": 120
        }

    def run(self, state: AgentState):
        print("--- Escalation Agent ---")
        messages = state['messages']
        last_message = messages[-1]['content'].lower()
        original_message = messages[-1]['content']
        user_id = state.get("user_id", "unknown_user")
        sentiment = state.get("sentiment", "Neutral")
        
        context = get_user_context(user_id)
        
        # Determine Priority
        priority = "Medium"
        if "urgent" in last_message or "critical" in last_message or "now" in last_message:
            priority = "High"
        if sentiment == "Frustrated":
            priority = "High"
        if context['vip']:
            priority = "Critical (VIP)"
        
        est_time = self.resolution_times.get(priority, 60)
        
        # Find workaround
        workaround = ""
        for keyword, suggestion in self.workarounds.items():
            if keyword in last_message:
                workaround = f"\n\n{suggestion}"
                break
        
        # Empathy tone
        if "furious" in last_message or "hate" in last_message or sentiment == "Frustrated":
            intro = "I am truly sorry for the frustration this has caused. We're treating this as a priority."
        elif context['vip']:
            intro = f"Welcome, {context['role']}. Your request is being prioritized immediately."
        else:
            intro = "I understand this needs attention. I'm escalating to our support team."
        
        # Create Jira Ticket
        jira_result = jira_create_ticket(
            summary=f"[IT Support] {original_message[:40]}...",
            description=f"**User:** {user_id}\n**Department:** {context['department']}\n**VIP:** {'Yes' if context['vip'] else 'No'}\n**Sentiment:** {sentiment}\n\n**Issue:**\n{original_message}\n\n---\n*Created by IT Support Genius AI*",
            priority=priority
        )
        
        # Build response
        response = f"""{intro}

**🎫 Jira Ticket Created:** {jira_result}

| Detail | Value |
|--------|-------|
| ⚡ **Priority** | {priority} |
| 🕐 **Est. Response** | {est_time} minutes |
| 👤 **User** | {user_id} |
| 🏢 **Department** | {context['department']} |
{workaround}

---
📲 **Slack Notification Sent:**
```
#it-support-{'urgent' if priority in ['High', 'Critical (VIP)'] else 'general'}
@it-oncall New escalation - {priority}
```

A human agent will reach out shortly.

🟢 *Confidence: 95%*"""
        
        audit_log = AuditLogger.log(state, "EscalationAgent", "ticket_created", {
            "jira": jira_result,
            "priority": priority,
            "vip": context['vip']
        })
        
        return {
            "messages": [{"role": "assistant", "content": response}],
            "next_agent": "END",
            "confidence": 0.95,
            "audit_log": audit_log
        }
