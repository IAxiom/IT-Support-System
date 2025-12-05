import os
from langgraph.graph import StateGraph, END
from state import AgentState
from agents.intake import IntakeAgent
from agents.knowledge import KnowledgeAgent
from agents.workflow import WorkflowAgent
from agents.escalation import EscalationAgent
from agents.log_analysis import LogAnalysisAgent

# Initialize Agents
intake_agent = IntakeAgent()
knowledge_agent = KnowledgeAgent()
workflow_agent = WorkflowAgent()
escalation_agent = EscalationAgent()
log_analysis_agent = LogAnalysisAgent()

# Define Nodes
def intake_node(state: AgentState):
    return intake_agent.run(state)

def knowledge_node(state: AgentState):
    return knowledge_agent.run(state)

def workflow_node(state: AgentState):
    return workflow_agent.run(state)

def escalation_node(state: AgentState):
    return escalation_agent.run(state)

def log_analysis_node(state: AgentState):
    return log_analysis_agent.run(state)

# Define Routing Logic
def route_intake(state: AgentState):
    next_agent = state.get("next_agent")
    if next_agent == "KnowledgeAgent":
        return "knowledge"
    elif next_agent == "WorkflowAgent":
        return "workflow"
    elif next_agent == "LogAnalysisAgent":
        return "log_analysis"
    elif next_agent == "EscalationAgent":
        return "escalation"
    else:
        return "knowledge" # Default

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("intake", intake_node)
workflow.add_node("knowledge", knowledge_node)
workflow.add_node("workflow", workflow_node)
workflow.add_node("escalation", escalation_node)
workflow.add_node("log_analysis", log_analysis_node)

workflow.set_entry_point("intake")

workflow.add_conditional_edges(
    "intake",
    route_intake,
    {
        "knowledge": "knowledge",
        "workflow": "workflow",
        "escalation": "escalation",
        "log_analysis": "log_analysis"
    }
)

workflow.add_edge("knowledge", END)
workflow.add_edge("workflow", END)
workflow.add_edge("escalation", END)
workflow.add_edge("log_analysis", END)

app = workflow.compile()

if __name__ == "__main__":
    print("Starting IT Support Agent System...")
    
    # Test Case 1: VPN Issue
    print("\n--- Test Case 1: VPN Issue ---")
    initial_state = {"messages": [{"role": "user", "content": "I can't connect to the VPN"}], "user_id": "user123"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])

    # Test Case 2: Password Policy
    print("\n--- Test Case 2: Password Policy ---")
    initial_state = {"messages": [{"role": "user", "content": "What is the password policy?"}], "user_id": "user123"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])

    # Test Case 3: Escalation
    print("\n--- Test Case 3: Escalation ---")
    initial_state = {"messages": [{"role": "user", "content": "I am very frustrated and need a human!"}], "user_id": "user123"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])

    # Test Case 4: Log Analysis (Advanced - Dev)
    print("\n--- Test Case 4: Log Analysis (Dev) ---")
    initial_state = {"messages": [{"role": "user", "content": "Can you check the system logs for errors?"}], "user_id": "user_dev"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])

    # Test Case 5: Log Analysis (Creative - Hacker)
    print("\n--- Test Case 5: Log Analysis (Security Breach) ---")
    initial_state = {"messages": [{"role": "user", "content": "Something weird is happening with my account."}], "user_id": "user_hacker"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])

    # Test Case 6: Creative RAG (Quantum)
    print("\n--- Test Case 6: Creative RAG (Quantum Policy) ---")
    initial_state = {"messages": [{"role": "user", "content": "How do I access the Q-1000 workstation?"}], "user_id": "user_scientist"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])

    # Test Case 7: Software Provisioning (Workflow)
    print("\n--- Test Case 7: Software Provisioning ---")
    initial_state = {"messages": [{"role": "user", "content": "I need a license for VS Code."}], "user_id": "user_dev"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])

    # Test Case 9: Identity (MFA Reset)
    print("\n--- Test Case 9: Identity (MFA Reset) ---")
    initial_state = {"messages": [{"role": "user", "content": "I lost my phone, reset my 2FA."}], "user_id": "user_mfa"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])

    # Test Case 10: Network (Server Reboot)
    print("\n--- Test Case 10: Network (Server Reboot) ---")
    initial_state = {"messages": [{"role": "user", "content": "Reboot the dev server."}], "user_id": "user_dev"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])

    # Test Case 12: Intake (Sentiment Auto-Escalation)
    print("\n--- Test Case 12: Intake (Sentiment Auto-Escalation) ---")
    initial_state = {"messages": [{"role": "user", "content": "I am absolutely furious! Nothing is working and I hate this system!"}], "user_id": "user_angry"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])

    # Test Case 14: Dynamic Workflow (LLM Tool Selection)
    print("\n--- Test Case 14: Dynamic Workflow (LLM Tool Selection) ---")
    initial_state = {"messages": [{"role": "user", "content": "I need a new mouse for my desk."}], "user_id": "user_dev"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])

    # Test Case 15: Creative Intake (VIP Auto-Escalation)
    print("\n--- Test Case 15: Creative Intake (VIP Auto-Escalation) ---")
    initial_state = {"messages": [{"role": "user", "content": "My email is down and it is critical!"}], "user_id": "user_ceo"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])
    
    # Test Case 16: Empathy Engine
    print("\n--- Test Case 16: Empathy Engine ---")
    initial_state = {"messages": [{"role": "user", "content": "I hate this system! It never works!"}], "user_id": "user_angry"}
    result = app.invoke(initial_state)
    print("Final Result:", result['messages'][-1]['content'])
