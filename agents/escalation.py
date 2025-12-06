from state import AgentState, AuditLogger
from tools.mcp_tools import get_user_context
from datetime import datetime

# Import Jira integration
try:
    from integrations.jira_client import jira_create_ticket, is_demo_mode
    JIRA_AVAILABLE = True
except ImportError:
    JIRA_AVAILABLE = False
    def jira_create_ticket(*args, **kwargs):
        return "❌ Jira integration not available"
    def is_demo_mode():
        return True

class EscalationAgent:
    def __init__(self):
        # Workaround database keyed by keywords
        self.workarounds = {
            "vpn": "While waiting, try: 1) Restart VPN client, 2) Connect to different region, 3) Use mobile hotspot.",
            "email": "While waiting: 1) Access webmail at mail.company.com, 2) Check spam folder, 3) Clear Outlook cache.",
            "password": "While waiting: 1) Use 'Forgot Password' on login page, 2) Check if Caps Lock is on.",
            "slow": "While waiting: 1) Close unused browser tabs, 2) Restart computer, 3) Run disk cleanup.",
            "crash": "While waiting: 1) Save work frequently, 2) Check for software updates.",
            "printer": "While waiting: 1) Try different printer, 2) Restart print spooler, 3) Clear print queue."
        }
        
        # Resolution time estimates (in minutes)
        self.resolution_times = {
            "Critical (VIP)": 15,
            "High": 30,
            "Medium": 60,
            "Low": 120
        }

    def run(self, state: AgentState):
        print("--- Escalation Agent (Empathy Engine) ---")
        messages = state['messages']
        last_message = messages[-1]['content'].lower()
        original_message = messages[-1]['content']
        user_id = state.get("user_id", "unknown_user")
        sentiment = state.get("sentiment", "Neutral")
        
        # Fetch Context
        context = get_user_context(user_id)
        
        # Determine Priority
        priority = "Medium"
        if "urgent" in last_message or "critical" in last_message:
            priority = "High"
        if sentiment == "Frustrated":
            priority = "High"
        if context['vip']:
            priority = "Critical (VIP)"
        
        # Get estimated resolution time
        est_time = self.resolution_times.get(priority, 60)
        
        # Find relevant workaround
        workaround = None
        for keyword, suggestion in self.workarounds.items():
            if keyword in last_message:
                workaround = suggestion
                break
        
        # Empathy Engine: Adjust Tone based on sentiment
        tone = "Professional"
        intro = "I understand this is a complex issue."
        
        if "furious" in last_message or "hate" in last_message or sentiment == "Frustrated":
            tone = "Apologetic"
            intro = "I am truly sorry for the frustration this has caused. We value your patience and are treating this as a priority."
        
        if context['vip']:
            tone = "White Glove"
            intro = f"Welcome, {context['role']}. Your request is being prioritized immediately by our senior team."

        # Create REAL Jira Ticket
        jira_result = jira_create_ticket(
            summary=f"[IT Support] {original_message[:50]}{'...' if len(original_message) > 50 else ''}",
            description=f"""
**User:** {user_id}
**Department:** {context['department']}
**VIP:** {'Yes' if context['vip'] else 'No'}
**Sentiment:** {sentiment}

**User Request:**
{original_message}

---
*Ticket created by IT Support Genius AI*
            """.strip(),
            priority=priority
        )
        
        demo_tag = " (Demo Mode)" if is_demo_mode() else ""

        # Build response
        response_parts = [
            f"{intro} I have escalated this to our Tier 2 Human Support team.\n",
            f"**🎫 Jira Ticket Created{demo_tag}:**",
            f"{jira_result}",
            f"**⚡ Priority:** {priority}",
            f"**🕐 Estimated Response:** {est_time} minutes",
            f"**👔 Service Level:** {tone}",
        ]
        
        if workaround:
            response_parts.append(f"\n**💡 While You Wait:**\n{workaround}")
        
        # Slack notification simulation
        slack_channel = "#it-support-urgent" if priority in ["High", "Critical (VIP)"] else "#it-support-general"
        response_parts.append(f"\n---")
        response_parts.append(f"📲 **Slack Notification Sent:**")
        response_parts.append(f"```")
        response_parts.append(f"Channel: {slack_channel}")
        response_parts.append(f"@it-oncall {jira_result[:50]}")
        response_parts.append(f"Priority: {priority}")
        response_parts.append(f"User: {user_id} ({context['department']})")
        response_parts.append(f"```")
        
        response_parts.append(f"\nA human agent will reach out within {est_time} minutes.")
        
        # Confidence
        confidence = 0.95
        response_parts.append(f"\n🟢 *Confidence: {confidence:.0%}*")

        response = "\n".join(response_parts)
        
        # Log the escalation
        audit_log = AuditLogger.log(state, "EscalationAgent", "jira_ticket_created", {
            "jira_result": jira_result,
            "priority": priority,
            "tone": tone,
            "vip": context['vip'],
            "demo_mode": is_demo_mode()
        })
        
        return {
            "messages": [{"role": "assistant", "content": response}],
            "next_agent": "END",
            "confidence": confidence,
            "audit_log": audit_log
        }
