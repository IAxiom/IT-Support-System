
from typing import TypedDict, Annotated, List, Union
import operator

class AgentState(TypedDict):
    messages: Annotated[List[dict], operator.add]
    next_agent: str
    current_context: dict
    user_id: str
