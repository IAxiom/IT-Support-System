from state import AgentState, AuditLogger
from utils.llm import analyze_request, get_llm
from tools.mcp_tools import get_user_context
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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
        
        # 2. Generate conversation summary for multi-turn context
        conversation_summary = self._generate_conversation_summary(messages)
        
        # 3. Analyze request with context awareness
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
        
        # Log the routing decision
        audit_log = AuditLogger.log(state, "IntakeAgent", "request_routed", {
            "intent": intent,
            "sentiment": sentiment,
            "urgency": urgency,
            "vip": context['vip']
        })
            
        return {
            "next_agent": intent, 
            "entities": entities, 
            "sentiment": sentiment, 
            "urgency": urgency,
            "conversation_summary": conversation_summary,
            "audit_log": audit_log
        }
    
    def _generate_conversation_summary(self, messages: list) -> str:
        """Generate a summary of the conversation for multi-turn context"""
        if len(messages) <= 1:
            return ""
        
        # Get last few messages for context
        recent_messages = messages[-5:]  # Last 5 messages
        
        try:
            llm = get_llm()
            template = """
            Summarize this IT support conversation in 1-2 sentences for context:
            
            {conversation}
            
            Summary (focus on the user's issue and any actions taken):
            """
            
            conversation_text = "\n".join([
                f"{m['role'].upper()}: {m['content'][:200]}" 
                for m in recent_messages
            ])
            
            prompt = ChatPromptTemplate.from_template(template)
            chain = prompt | llm | StrOutputParser()
            
            summary = chain.invoke({"conversation": conversation_text})
            print(f"Conversation Summary: {summary[:100]}...")
            return summary.strip()
            
        except Exception as e:
            print(f"Summary generation failed: {e}")
            # Fallback: just return the last message
            if len(messages) > 1:
                return f"Previous topic: {messages[-2]['content'][:100]}"
            return ""
