
from state import AgentState
from tools.mcp_tools import get_user_context
import random

class EscalationAgent:
    def __init__(self):
        pass

    def run(self, state: AgentState):
        print("--- Escalation Agent (Empathy Engine) ---")
        messages = state['messages']
        last_message = messages[-1]['content']
        user_id = state.get("user_id", "unknown_user")
        
        # Fetch Context
        context = get_user_context(user_id)
        
        # Generate Ticket ID
        ticket_id = f"INC-{random.randint(10000, 99999)}"
        
        # Determine Priority
        priority = "High" if "urgent" in last_message.lower() or "critical" in last_message.lower() else "Medium"
        if context['vip']: priority = "Critical (VIP)"
        
        # Empathy Engine: Adjust Tone
        tone = "Professional"
        intro = "I understand this is a complex issue."
        
        if "furious" in last_message.lower() or "hate" in last_message.lower():
            tone = "Apologetic"
            intro = "I am truly sorry for the frustration this has caused. We value your patience."
        
        if context['vip']:
            tone = "White Glove"
            intro = f"Welcome, {context['role']}. We are prioritizing your request immediately."

        response = (
            f"{intro} I have escalated this to our Tier 2 Human Support team.\n\n"
            f"**Ticket Created:** #{ticket_id}\n"
            f"**Priority:** {priority}\n"
            f"**Service Level:** {tone} Response\n"
            f"**Summary:** User reported '{last_message[:50]}...'\n\n"
            f"A human agent will reach out to you via Slack within 15 minutes."
        )
        
        return {
            "messages": [{"role": "assistant", "content": response}],
            "next_agent": "END"
        }
