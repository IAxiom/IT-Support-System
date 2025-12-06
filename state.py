from typing import TypedDict, List, Any, Optional

class AgentState(TypedDict, total=False):
    messages: List[dict]
    user_id: str
    next_agent: str
    routing_path: List[str]  # Track agent traversal for visualization
    entities: dict           # Extracted entities from intake
    sentiment: str           # User sentiment (Positive/Neutral/Negative/Frustrated)
    urgency: str             # Issue urgency (Low/Medium/High/Critical)

    current_context: dict
