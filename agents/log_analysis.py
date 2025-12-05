from state import AgentState
from tools.mcp_tools import fetch_recent_logs, create_ticket
from utils.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class LogAnalysisAgent:
    def __init__(self):
        pass

    def run(self, state: AgentState):
        print("--- Log Analysis Agent ---")
        user_id = state.get("user_id", "unknown_user")
        
        # 1. Fetch Logs (Simulating MCP tool use)
        logs = fetch_recent_logs(user_id)
        
        # 2. Analyze with LLM
        llm = get_llm()
        template = """
        You are a Senior Site Reliability Engineer. Analyze the following system logs and identify the root cause of the failure.
        
        Logs:
        {logs}
        
        Provide a concise diagnosis and a recommended fix.
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm | StrOutputParser()
        
        try:
            diagnosis = chain.invoke({"logs": logs})
        except Exception as e:
            diagnosis = f"Error analyzing logs: {e}"
            
        # 3. Auto-Create Ticket if critical (Simulating MCP)
        if "CRITICAL" in logs or "Fatal" in diagnosis:
            ticket_result = create_ticket(
                title=f"Automated Log Analysis: {user_id}",
                description=diagnosis,
                priority="High"
            )
            response = f"{diagnosis}\n\nI have automatically created a support ticket for this critical issue: {ticket_result}"
        else:
            response = diagnosis
            
        return {
            "messages": [{"role": "assistant", "content": response}],
            "next_agent": "END"
        }
