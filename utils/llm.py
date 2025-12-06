import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Check for API key once at module load
_API_KEY_PRESENT = bool(os.environ.get("GOOGLE_API_KEY"))
if not _API_KEY_PRESENT:
    print("⚠️ Warning: GOOGLE_API_KEY not found. LLM features will use fallback mode.")

def get_llm():
    """Get the LLM instance. Raises early if no API key."""
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not configured")
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)


class RequestAnalysis(BaseModel):
    intent: str = Field(description="The target agent: WorkflowAgent, LogAnalysisAgent, KnowledgeAgent, or EscalationAgent")
    sentiment: str = Field(description="User sentiment: Positive, Neutral, Negative, or Frustrated")
    urgency: str = Field(description="Issue urgency: Low, Medium, High, Critical")
    entities: dict = Field(description="Extracted entities like user_id, device, error_code, software_name")


def analyze_request(message: str) -> dict:
    """
    Analyzes user request for intent, sentiment, and entities.
    Falls back to keyword matching if LLM unavailable.
    """
    # Keyword-based fallback for when LLM is unavailable
    message_lower = message.lower()
    
    # Keyword-based intent detection
    if any(word in message_lower for word in ["angry", "furious", "frustrated", "hate", "worst"]):
        fallback_intent = "EscalationAgent"
        fallback_sentiment = "Frustrated"
    elif any(word in message_lower for word in ["log", "error", "security", "suspicious", "hack", "breach"]):
        fallback_intent = "LogAnalysisAgent"
        fallback_sentiment = "Neutral"
    elif any(word in message_lower for word in ["reset", "unlock", "password", "mfa", "vpn", "reboot", "order", "install"]):
        fallback_intent = "WorkflowAgent"
        fallback_sentiment = "Neutral"
    else:
        fallback_intent = "KnowledgeAgent"
        fallback_sentiment = "Neutral"
    
    # Urgency detection
    if any(word in message_lower for word in ["urgent", "critical", "emergency", "now", "asap"]):
        fallback_urgency = "High"
    else:
        fallback_urgency = "Medium"
    
    fallback = {
        "intent": fallback_intent,
        "sentiment": fallback_sentiment,
        "urgency": fallback_urgency,
        "entities": {}
    }
    
    # Try LLM if available
    if not _API_KEY_PRESENT:
        print(f"[Fallback] Intent: {fallback_intent} (keyword-based)")
        return fallback
    
    try:
        llm = get_llm()
        parser = JsonOutputParser(pydantic_object=RequestAnalysis)
        
        template = """
        You are an AI Intake Specialist for IT Support. Analyze the user's message.
        
        1. **Classify Intent**:
           - WorkflowAgent: Actionable technical tasks (VPN, Hardware, Software, Identity, Network).
           - LogAnalysisAgent: Logs, errors, crashes, security alerts (ransomware, phishing).
           - KnowledgeAgent: Policy questions, "how to", general info.
           - EscalationAgent: Human request, high frustration, complex unknown issues.
           
        2. **Analyze Sentiment**: Positive, Neutral, Negative, or Frustrated.
        3. **Assess Urgency**: Low, Medium, High, Critical.
        4. **Extract Entities**: user_id, device, software, error codes, location, etc.
        
        User Message: {message}
        
        {format_instructions}
        """
        
        prompt = ChatPromptTemplate.from_template(template, partial_variables={"format_instructions": parser.get_format_instructions()})
        chain = prompt | llm | parser
        return chain.invoke({"message": message})
        
    except Exception as e:
        print(f"LLM Analysis Error: {e}")
        return fallback


def mock_llm_rag_response(query: str, context: str) -> str:
    """
    Generates a RAG response using Gemini.
    Falls back to context-based response if LLM unavailable.
    """
    # Fallback: return most relevant context snippet
    if not _API_KEY_PRESENT or not context.strip():
        if context.strip():
            # Return first 500 chars of context as the answer
            snippet = context[:500].strip()
            if len(context) > 500:
                snippet += "..."
            return f"Based on our documentation:\n\n{snippet}\n\n🟡 *Confidence: 60%* (LLM unavailable - showing raw docs)"
        return "I don't have information about this in my knowledge base. Please contact IT support at support@company.com or (555) 123-4567.\n\n🔴 *Confidence: 20%*"
    
    try:
        llm = get_llm()
        template = """
        You are a helpful IT Support Assistant. Answer the user's question based ONLY on the following context.
        If the answer is not in the context, say you don't know and suggest escalating.
        
        Context:
        {context}
        
        Question: {query}
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"context": context, "query": query})
        
    except Exception as e:
        print(f"LLM Error: {e}")
        # Better fallback - show context snippet
        if context.strip():
            snippet = context[:300].strip()
            return f"Here's what I found in our docs:\n\n{snippet}\n\n⚠️ *Please verify this information with IT support.*"
        return "I'm having trouble processing your request. Please contact IT support at (555) 123-4567.\n\n🔴 *Confidence: 20%*"


class ToolSelection(BaseModel):
    tool_name: str = Field(description="The name of the tool to call (or 'None' if no tool matches)")
    arguments: dict = Field(description="Arguments for the tool")
    reasoning: str = Field(description="Why this tool was selected")


def select_tool(message: str, tools_description: str) -> dict:
    """
    Selects the best tool to handle the user's request.
    Falls back to keyword matching if LLM unavailable.
    """
    message_lower = message.lower()
    
    # Keyword-based tool selection fallback
    tool_keywords = {
        "check_vpn_status": ["vpn", "connect", "network"],
        "unlock_account": ["unlock", "locked", "lockout"],
        "reset_mfa": ["mfa", "2fa", "authenticator", "two-factor"],
        "provision_license": ["license", "software", "install"],
        "check_hardware_eligibility": ["laptop", "refresh", "upgrade", "old"],
        "order_peripheral": ["mouse", "keyboard", "monitor", "peripheral", "order"],
        "reboot_server": ["reboot", "server", "restart"],
        "onboard_user": ["onboard", "new hire", "new employee"],
        "offboard_user": ["offboard", "terminate", "disable account", "leaving"],
        "grant_temp_admin": ["admin", "sudo", "elevated", "temporary access"],
    }
    
    # Find matching tool by keywords
    fallback_tool = "None"
    for tool_name, keywords in tool_keywords.items():
        if any(kw in message_lower for kw in keywords):
            fallback_tool = tool_name
            break
    
    fallback = {
        "tool_name": fallback_tool,
        "arguments": {},
        "reasoning": "Keyword-based selection (LLM unavailable)"
    }
    
    if not _API_KEY_PRESENT:
        print(f"[Fallback] Tool: {fallback_tool} (keyword-based)")
        return fallback
    
    try:
        llm = get_llm()
        parser = JsonOutputParser(pydantic_object=ToolSelection)
        
        template = """
        You are an AI Workflow Orchestrator. Select the appropriate tool to handle the user's request.
        
        Available Tools:
        {tools_description}
        
        User Message: {message}
        
        Return the tool name and arguments. If no tool matches, return 'None'.
        
        {format_instructions}
        """
        
        prompt = ChatPromptTemplate.from_template(template, partial_variables={"format_instructions": parser.get_format_instructions()})
        chain = prompt | llm | parser
        return chain.invoke({"message": message, "tools_description": tools_description})
        
    except Exception as e:
        print(f"LLM Tool Selection Error: {e}")
        return fallback
