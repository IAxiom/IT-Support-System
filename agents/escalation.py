
from state import AgentState
from tools.mcp_tools import get_user_context
import random

class EscalationAgent:
    def __init__(self):
        # Workaround database keyed by keywords
        self.workarounds = {
            "vpn": "While waiting, you can try: 1) Restart your VPN client, 2) Connect to a different region, 3) Use mobile hotspot temporarily.",
            "email": "While waiting, you can: 1) Access webmail at mail.company.com, 2) Check spam folder, 3) Clear Outlook cache.",
            "password": "While waiting, try: 1) Use 'Forgot Password' on the login page, 2) Check if Caps Lock is on.",
            "slow": "While waiting, try: 1) Close unused browser tabs, 2) Restart your computer, 3) Run disk cleanup.",
            "crash": "While waiting, try: 1) Save your work frequently, 2) Check for software updates, 3) Increase RAM allocation if possible."
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
        user_id = state.get("user_id", "unknown_user")
        sentiment = state.get("sentiment", "Neutral")
        
        # Fetch Context
        context = get_user_context(user_id)
        
        # Generate Ticket ID
        ticket_id = f"INC-{random.randint(10000, 99999)}"
        
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

        # Build response
        response_parts = [
            f"{intro} I have escalated this to our Tier 2 Human Support team.\n",
            f"**🎫 Ticket Created:** #{ticket_id}",
            f"**⚡ Priority:** {priority}",
            f"**🕐 Estimated Response:** {est_time} minutes",
            f"**👔 Service Level:** {tone}",
            f"**📝 Summary:** \"{messages[-1]['content'][:80]}{'...' if len(messages[-1]['content']) > 80 else ''}\"",
        ]
        
        if workaround:
            response_parts.append(f"\n**💡 While You Wait:**\n{workaround}")
        
        response_parts.append(f"\n---\n📲 *Notification sent to #it-support-urgent on Slack*\nA human agent will reach out within {est_time} minutes.")

        response = "\n".join(response_parts)
        
        return {
            "messages": [{"role": "assistant", "content": response}],
            "next_agent": "END"
        }
