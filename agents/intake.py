
from state import AgentState
from utils.llm import analyze_request
from tools.mcp_tools import get_user_context

class IntakeAgent:
    def __init__(self):
        pass

    def run(self, state: AgentState):
        print("--- Intake Agent (Creative) ---")
        messages = state['messages']
        last_message = messages[-1]['content']
        user_id = state.get("user_id", "unknown_user")
        
        # 1. Fetch Predictive Context
        context = get_user_context(user_id)
        
        # 2. Analyze request with context awareness (conceptually)
        analysis = analyze_request(last_message)
        
        intent = analysis.get("intent", "KnowledgeAgent")
        sentiment = analysis.get("sentiment", "Neutral")
        urgency = analysis.get("urgency", "Medium")
        entities = analysis.get("entities", {})
        
        print(f"Analysis: Intent={intent} | Sentiment={sentiment} | Urgency={urgency}")
        print(f"Context: {context['location']} | VIP: {context['vip']}")
        
        # Logic: VIPs get auto-escalated for High urgency (not just Critical)
        if context['vip'] and urgency in ["High", "Critical"]:
             print(">> VIP Auto-Escalation <<")
             intent = "EscalationAgent"
        
        # Logic: Auto-escalate if Frustrated
        elif sentiment == "Frustrated" or urgency == "Critical":
            print(">> Auto-Escalating due to Sentiment/Urgency <<")
            intent = "EscalationAgent"
            
        return {"next_agent": intent, "entities": entities, "sentiment": sentiment, "urgency": urgency}
