import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_llm():
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found.")
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class RequestAnalysis(BaseModel):
    intent: str = Field(description="The target agent: WorkflowAgent, LogAnalysisAgent, KnowledgeAgent, or EscalationAgent")
    sentiment: str = Field(description="User sentiment: Positive, Neutral, Negative, or Frustrated")
    urgency: str = Field(description="Issue urgency: Low, Medium, High, Critical")
    entities: dict = Field(description="Extracted entities like user_id, device, error_code, software_name")

def analyze_request(message: str) -> dict:
    """
    Analyzes user request for intent, sentiment, and entities using Gemini.
    """
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
    
    try:
        return chain.invoke({"message": message})
    except Exception as e:
        print(f"LLM Analysis Error: {e}")
        # Fallback
        return {
            "intent": "KnowledgeAgent",
            "sentiment": "Neutral",
            "urgency": "Medium",
            "entities": {}
        }

def mock_llm_rag_response(query: str, context: str) -> str:
    """
    Generates a RAG response using Gemini.
    """
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
    
    try:
        return chain.invoke({"context": context, "query": query})
    except Exception as e:
        print(f"LLM Error: {e}")
        return "I'm having trouble connecting to my brain right now. Please try again."

class ToolSelection(BaseModel):
    tool_name: str = Field(description="The name of the tool to call (or 'None' if no tool matches)")
    arguments: dict = Field(description="Arguments for the tool")
    reasoning: str = Field(description="Why this tool was selected")

def select_tool(message: str, tools_description: str) -> dict:
    """
    Selects the best tool to handle the user's request.
    """
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
    
    try:
        return chain.invoke({"message": message, "tools_description": tools_description})
    except Exception as e:
        print(f"LLM Tool Selection Error: {e}")
        return {"tool_name": "None", "arguments": {}, "reasoning": "Error"}
